"""
Path: src/configuration/webhook_configurator.py
"""
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.services.telegram_service import TelegramService
from src.utils.logging.dependency_injection import get_logger
from src.utils.error_handler import log_warning

__all__ = ['WebhookConfigurator']

class WebhookConfigurator:
    "Clase que maneja la configuración del webhook"
    def __init__(self, use_colors: bool):

        self.interface = Interface(use_colors=use_colors)
        self.presentation_service = PresentationService(self.interface)
        self.telegram_service = TelegramService()

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

    def configure_webhook(self, base_url, webhook_endpoint="webhook", attempts=0, max_attempts=3):
        "Configura el webhook con la URL proporcionada"
        logger_local = get_logger("webhook_configurator")
        if attempts >= max_attempts:
            self.presentation_service.show_warning_message("Número máximo de intentos alcanzado")
            return False, "Número máximo de intentos alcanzado"
        # Nuevo mensaje informativo del intento actual
        logger_local.info("Configurando webhook: intento %d de %d", attempts + 1, max_attempts)
        self.presentation_service.show_debug_info(
            f"Intentando configurar webhook (intento {attempts + 1} de {max_attempts})..."
        )
        self.presentation_service.notify_operation_start("Configuración de webhook")
        webhook_url = f"{base_url}/{webhook_endpoint}"
        self.presentation_service.show_debug_info(
            f"Intentando configurar webhook en: {webhook_url}"
        )
        try:
            success, _ = self.telegram_service.configure_webhook(
                webhook_url
            )
        except (ConnectionError, TimeoutError) as e:
            self.presentation_service.show_error_message(f"Excepción al configurar webhook: {e}")
            return False, str(e)
        if success:
            self.presentation_service.show_webhook_status(True, webhook_url)
            return True, None
        else:
            self.presentation_service.show_webhook_status(False)
            if self.presentation_service.ask_for_retry("configuración del webhook"):
                return self.configure_webhook(base_url, webhook_endpoint, attempts+1, max_attempts)
            else:
                self.presentation_service.show_warning_message(
                    "Webhook no configurado por decisión del usuario"
                )
                return False, "Webhook no configurado por decisión del usuario"

    def try_configure_webhook(self):
        " Intenta configurar el webhook y muestra mensajes de estado "
        public_url, _ = self.get_public_url()
        if not public_url:
            return False
        success, _ = self.configure_webhook(public_url)
        return success
