"""
Path: src/configuration/webhook_configurator.py
"""
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.services.telegram_service import TelegramService

__all__ = ['WebhookConfigurator']

class WebhookConfigurator:
    "Clase que maneja la configuración del webhook"
    def __init__(self, use_colors: bool):

        self.interface = Interface(use_colors=use_colors)
        self.presentation_service = PresentationService(self.interface)
        self.telegram_service = TelegramService()

    def get_public_url(self):
        "Solicita al usuario la URL pública para configurar el webhook"
        public_url = self.presentation_service.ask_for_public_url()
        if not public_url:
            self.presentation_service.show_message_send_error("No se proporcionó una URL")
            return None, "No se proporcionó una URL"
        if not public_url.startswith(("http://", "https://")):
            self.presentation_service.show_message_send_error(
                "La URL debe comenzar con http:// o https://"
            )
            return None, "La URL debe comenzar con http:// o https://"
        return public_url, None

    def configure_webhook(self, base_url, webhook_endpoint="webhook"):
        "Configura el webhook con la URL proporcionada"
        self.presentation_service.notify_operation_start("Configuración de webhook")
        webhook_url = f"{base_url}/{webhook_endpoint}"
        self.presentation_service.show_debug_info(
            f"Intentando configurar webhook en: {webhook_url}"
        )
        success, _ = self.telegram_service.configure_webhook(
            webhook_url
        )
        if success:
            self.presentation_service.show_webhook_status(True, webhook_url)
            return True, None
        else:
            self.presentation_service.show_webhook_status(False)
            if self.presentation_service.ask_for_retry("configuración del webhook"):
                return self.configure_webhook(base_url, webhook_endpoint)
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
