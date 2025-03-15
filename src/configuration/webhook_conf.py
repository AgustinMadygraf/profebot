"""
Path: src/configuration/webhook_conf.py

Nota de actualización:
    La configuración del webhook se centraliza mediante el servicio WebhookConfigService
    (ubicado en src/services/webhook_config_service.py). Este servicio se encarga de:
      • Obtener la URL pública (primero intentando con ngrok,
        de no obtenerla, solicitándola al usuario).
      • Verificar el estado actual del webhook configurado en Telegram.
      • Configurar el webhook en Telegram de ser necesario.
    Este nuevo flujo mejora la modularidad y facilita el mantenimiento del sistema.
"""

from src.services.telegram_service import TelegramService
from src.utils.logging.simple_logger import get_logger
from src.services.webhook_config_service import WebhookConfigService

class WebhookConfigurator:
    "Clase que maneja la configuración del webhook usando WebhookConfigService"

    def __init__(self):
        self.telegram_service = TelegramService()
        self.logger = get_logger()
        self.logger.debug("WebhookConfigurator inicializado")

    # Métodos duplicados removidos: get_public_url y configure_webhook

    def try_configure_webhook(self):
        "Intenta configurar el webhook delegando en WebhookConfigService"
        self.logger.info("Iniciando configuración del webhook mediante WebhookConfigService")
        config_service = WebhookConfigService()
        result = config_service.run_configuration()
        if not result:
            self.logger.error("Fallo en la configuración del webhook.")
        return result
