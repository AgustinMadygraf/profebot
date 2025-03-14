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

import requests
from src.services.telegram_service import TelegramService
from src.utils.logging.simple_logger import get_logger
from src.services.webhook_config_service import WebhookConfigService

class WebhookConfigurator:
    "Clase que maneja la configuración del webhook"

    def __init__(self):
        self.telegram_service = TelegramService()
        self.logger = get_logger()
        self.logger.debug("WebhookConfigurator inicializado")

    def get_public_url(self):
        "Solicita al usuario la URL pública para configurar el webhook"
        self.logger.debug("Solicitando URL pública al usuario")
        public_url = input("Ingrese la URL pública para configurar el webhook: ").strip()
        if public_url:
            self.logger.debug("URL pública ingresada: %s", public_url)
        else:
            self.logger.warning("No se proporcionó una URL")
            return None, "No se proporcionó una URL"
        if not public_url.startswith(("http://", "https://")):
            self.logger.warning("La URL debe comenzar con http:// o https://")
            return None, "La URL debe comenzar con http:// o https://"
        return public_url, None

    def configure_webhook(self, base_url, webhook_endpoint="webhook"):
        "Configura el webhook con la URL proporcionada"
        webhook_url = f"{base_url}/{webhook_endpoint}"
        self.logger.debug("Configurando webhook en la URL: %s", webhook_url)
        try:
            success, error = self.telegram_service.configure_webhook(webhook_url)
            if success:
                self.logger.info("Webhook configurado correctamente en: %s", webhook_url)
                return True, None
            else:
                self.logger.error("Error configurando webhook: %s", error)
                return False, error
        except requests.exceptions.RequestException as e:
            self.logger.exception("Excepción al configurar webhook: %s", e)
            return False, str(e)

    def try_configure_webhook(self):
        "Intenta configurar el webhook, solicitando la URL pública si es necesario"
        self.logger.info("Iniciando configuración del webhook mediante WebhookConfigService")
        config_service = WebhookConfigService()
        result = config_service.run_configuration()
        if not result:
            self.logger.error("Fallo en la configuración del webhook.")
        return result
