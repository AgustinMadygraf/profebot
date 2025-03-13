"""
Path: src/configuration/webhook_configurator.py
"""

import time
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.services.telegram_service import TelegramService
from src.utils.logging.dependency_injection import get_logger
from src.utils.error_handler import log_warning, log_exception
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
        # Debug: registrar inicialización del objeto
        get_logger("webhook_configurator").debug(
            "WebhookConfigurator initialized with use_colors: %s", use_colors
        )

    def set_notification_callback(self, event: str, callback):
        """Registra un callback para un evento de notificación.
           event: nombre del evento ('debug', 'operation_start', 'status', 'warning',
                  'error', 'retry_info', etc.)
           callback: función que recibirá (message, *args, **kwargs)
        """
        get_logger("webhook_configurator").debug("Registering callback for event: %s", event)
        self.notification_callbacks[event] = callback

    def _notify(self, event: str, message: str, *args, **kwargs):
        """Notifica de forma unificada utilizando PresentationService.notify()."""
        get_logger("webhook_configurator").debug("Notifying event: %s, message: %s", event, message)
        if event in self.notification_callbacks:
            self.notification_callbacks[event](message, *args, **kwargs)
        else:
            self.presentation_service.notify(event, message, *args, **kwargs)

    def get_public_url(self):
        "Solicita al usuario la URL pública para configurar el webhook"
        logger_local = get_logger("webhook_configurator")
        logger_local.debug("Solicitando URL pública al usuario")
        public_url = self.presentation_service.ask_for_public_url()
        if public_url:
            logger_local.debug("URL pública ingresada: %s", public_url)
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

    def _calculate_delay(self, attempt, base_delay):
        "Calcula el delay de reintento usando backoff exponencial"
        delay = base_delay * (2 ** attempt)
        get_logger("webhook_configurator").debug(
            "Calculated delay: %s seconds for attempt: %s", delay, attempt
        )
        return delay

    def _perform_retry_wait(self, attempts, max_attempts, base_delay):
        delay = self._calculate_delay(attempts, base_delay)
        get_logger("webhook_configurator").debug(
            "Intento %s fallido. Reintentando en %s segundos (Intento %s de %s)",
            attempts + 1, delay, attempts + 2, max_attempts
        )
        self._notify("retry_info", "", attempts, max_attempts, delay)
        dispatcher.dispatch(
            "retry_attempt", 
            attempt=attempts,
            max_attempts=max_attempts,
            delay=delay
        )
        get_logger("webhook_configurator").debug(
            "Esperando %s segundos antes del siguiente intento", delay
        )
        time.sleep(delay)
        get_logger("webhook_configurator").debug(
            "Finalizado sleep de %s segundos para el intento %s", 
            delay, attempts + 1
        )
        return delay

    def _should_retry_configuration(self):
        """
        Separa la lógica de confirmación de reintento para configurar el webhook.
        Retorna True si se debe reintentar; False en caso contrario.
        """
        return self.presentation_service.ask_for_retry("configuración del webhook")

    def configure_webhook(self, base_url, webhook_endpoint="webhook"):
        "Configura el webhook con la URL proporcionada utilizando un ciclo iterativo"
        logger_local = get_logger("webhook_configurator")
        config = get_config()
        max_attempts = config.get("max_retries", 3)
        base_delay = config.get("retry_delay", 5)
        attempts = 0
        webhook_url = f"{base_url}/{webhook_endpoint}"
        logger_local.debug("Iniciando configuración del webhook con URL: %s", webhook_url)
        while attempts < max_attempts:
            self._notify(
                "debug",
                (f"Intento {attempts + 1} de {max_attempts} para configurar "
                 f"webhook en: {webhook_url}")
            )
            self._notify("operation_start", "Configuración de webhook")
            success, _ = self._attempt_configure(webhook_url)
            if success:
                self._notify("status", webhook_url, True)
                dispatcher.dispatch("webhook_configured", url=webhook_url)
                return True, None
            self._notify("status", None, False)
            if not self._should_retry_configuration():
                self._notify("warning", "Webhook no configurado por decisión del usuario")
                dispatcher.dispatch("webhook_failed", error="Decisión de usuario")
                return False, "Webhook no configurado por decisión del usuario"
            _ = self._perform_retry_wait(attempts, max_attempts, base_delay)
            attempts += 1
        self._notify("warning", "Número máximo de intentos alcanzado")
        return False, "Número máximo de intentos alcanzado"

    def _attempt_configure(self, webhook_url):
        """Realiza un intento único de configuración del webhook.
           Retorna (True, None) si es exitoso, o (False, error_message) en caso de fallo.
        """
        logger_local = get_logger("webhook_configurator")
        logger_local.debug("Attempting to configure webhook at URL: %s", webhook_url)
        try:
            return self.telegram_service.configure_webhook(webhook_url)
        except (ConnectionError, TimeoutError) as e:
            # Nuevo: Uso de log_exception para manejo unificado de errores
            log_exception(
                self.presentation_service,
                logger_local,
                "Excepción al configurar webhook", 
                e
            )
            dispatcher.dispatch("webhook_failed", error=str(e))
            return False, str(e)

    def try_configure_webhook(self):
        "Intenta configurar el webhook y muestra mensajes de estado"
        logger_local = get_logger("webhook_configurator")
        public_url, _ = self.get_public_url()
        logger_local.debug("try_configure_webhook recibió URL: %s", public_url)
        if not public_url:
            return False
        success, _ = self.configure_webhook(public_url)
        return success
