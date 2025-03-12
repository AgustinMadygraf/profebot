"""
Path: src/configuration/webhook_configurator.py
"""

import time
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.services.telegram_service import TelegramService
from src.utils.logging.dependency_injection import get_logger
from src.utils.error_handler import log_warning
from src.utils.config.app_config import get_config
from src.utils.event_dispatcher import dispatcher

__all__ = ['WebhookConfigurator']

class WebhookConfigurator:
    "Clase que maneja la configuración del webhook"
    def __init__(self, use_colors: bool):

        self.interface = Interface(use_colors=use_colors)
        self.presentation_service = PresentationService(self.interface)
        self.telegram_service = TelegramService()
        # Nuevo: Diccionario para callbacks de notificación
        self.notification_callbacks = {}

    def set_notification_callback(self, event: str, callback):
        """Registra un callback para un evento de notificación.
           event: nombre del evento ('debug', 'operation_start', 'status', 'warning',
                  'error', 'retry_info', etc.)
           callback: función que recibirá (message, *args, **kwargs)
        """
        self.notification_callbacks[event] = callback

    def _notify(self, event: str, message: str, *args, **kwargs):
        """Notifica un evento usando el callback registrado o la PresentationService por defecto."""
        if event in self.notification_callbacks:
            self.notification_callbacks[event](message, *args, **kwargs)
        else:
            # Mapeo simple de evento a método en PresentationService
            method = {
                "debug": self.presentation_service.show_debug_info,
                "operation_start": self.presentation_service.notify_operation_start,
                "status": self.presentation_service.show_webhook_status,
                "warning": self.presentation_service.show_warning_message,
                "error": self.presentation_service.show_error_message,
                "retry_info": self.presentation_service.show_webhook_retry_info,
            }.get(event)
            if method:
                method(message, *args, **kwargs)
            else:
                # Se utiliza el método "info" de la interfaz asociada
                self.presentation_service.interface.info(message)

    def get_public_url(self):
        "Solicita al usuario la URL pública para configurar el webhook"
        logger_local = get_logger("webhook_configurator")
        public_url = self.presentation_service.ask_for_public_url()
        if not public_url:
            log_warning(
                self.presentation_service,
                logger_local,
                "Validación de URL", 
                "No se proporcionó una URL"
            )
            return None, "No se proporcionó una URL"
        if not public_url.startswith(("http://", "https://")):
            log_warning(
                self.presentation_service, logger_local, "Validación de URL",
                "La URL debe comenzar con http:// o https://"
            )
            return None, "La URL debe comenzar con http:// o https://"
        return public_url, None

    def configure_webhook(self, base_url, webhook_endpoint="webhook"):
        "Configura el webhook con la URL proporcionada utilizando un ciclo iterativo"
        config = get_config()
        max_attempts = config.get("max_retries", 3)
        base_delay = config.get("retry_delay", 5)  # Retardo base configurado
        attempts = 0
        webhook_url = f"{base_url}/{webhook_endpoint}"
        while attempts < max_attempts:
            self._notify(
                "debug",
                f"Intento {attempts + 1} de {max_attempts} para configurar "
                f"webhook en: {webhook_url}"
            )
            self._notify("operation_start", "Configuración de webhook")
            success, _ = self._attempt_configure(webhook_url)
            if success:
                self._notify("status", webhook_url, True)
                dispatcher.dispatch("webhook_configured", url=webhook_url)
                return True, None
            else:
                self._notify("status", None, False)
                if not self.presentation_service.ask_for_retry("configuración del webhook"):
                    self._notify("warning", "Webhook no configurado por decisión del usuario")
                    dispatcher.dispatch("webhook_failed", error="Decisión de usuario")
                    return False, "Webhook no configurado por decisión del usuario"
                else:
                    # Aplicar backoff exponencial y notificar el intento de reintento vía evento
                    delay = base_delay * (2 ** attempts)
                    self._notify("retry_info", "", attempts, max_attempts, delay)
                    dispatcher.dispatch(
                        "retry_attempt", 
                        attempt=attempts,
                        max_attempts=max_attempts,
                        delay=delay
                    )
                    time.sleep(delay)
            attempts += 1
        self._notify("warning", "Número máximo de intentos alcanzado")
        return False, "Número máximo de intentos alcanzado"

    def _attempt_configure(self, webhook_url):
        """Realiza un intento único de configuración del webhook.
           Retorna (True, None) si es exitoso, o (False, error_message) en caso de fallo.
        """
        try:
            return self.telegram_service.configure_webhook(webhook_url)
        except (ConnectionError, TimeoutError) as e:
            self._notify("error", f"Excepción al configurar webhook: {e}")
            dispatcher.dispatch("webhook_failed", error=str(e))
            return False, str(e)

    def try_configure_webhook(self):
        "Intenta configurar el webhook y muestra mensajes de estado"
        public_url, _ = self.get_public_url()
        if not public_url:
            return False
        success, _ = self.configure_webhook(public_url)
        return success
