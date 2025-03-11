"""
Path: src/webhook.py
"""

from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.utils.logging.dependency_injection import get_logger
from src.configuration.webhook_configurator import WebhookConfigurator

# Initialize logger
logger = get_logger("app_controller")

# Se crea una instancia con una interfaz por defecto (sin colores)
default_interface = Interface(use_colors=False)
presentation_service = PresentationService(default_interface)

def try_configure_webhook(use_colors):
    "Intenta configurar el webhook y muestra mensajes de estado"
    configurator = WebhookConfigurator(use_colors)
    success = configurator.try_configure_webhook()
    if success:
        configurator.presentation_service.show_debug_info("Webhook configurado correctamente")
    else:
        configurator.presentation_service.show_error_message("Error al configurar webhook")
    return success
