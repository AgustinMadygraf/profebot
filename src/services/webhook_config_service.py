"""
Path: src/services/webhook_config_service.py
"""

import requests
from src.services.telegram_service import TelegramService
from src.utils.logging.simple_logger import get_logger

class WebhookConfigService:
    "Clase que maneja la configuración del webhook"
    def __init__(self):
        self.logger = get_logger()
        self.telegram_service = TelegramService()

    def get_public_url(self):
        "Obtiene la URL pública para configurar el webhook"
        self.logger.info("Intentando obtener URL pública desde ngrok")
        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
            data = response.json()
            tunnels = data.get("tunnels", [])
            for tunnel in tunnels:
                if "public_url" in tunnel:
                    self.logger.debug("URL de ngrok encontrada: %s", tunnel["public_url"])
                    return tunnel["public_url"]
            self.logger.warning("No se encontró URL de ngrok válida")
        except requests.exceptions.RequestException as e:
            self.logger.debug("Error al obtener URL de ngrok: %s", e)
        public_url = input("Ingrese la URL pública para configurar el webhook: ").strip()
        if public_url and public_url.startswith(("http://", "https://")):
            return public_url
        self.logger.error("URL inválida proporcionada.")
        return None

    def verify_webhook(self, public_url):
        "Verifica si el webhook ya está configurado con la URL proporcionada"
        desired_webhook_url = f"{public_url}/webhook"
        success, info = self.telegram_service.get_webhook_info()
        if success and info.get("result", {}).get("url", "") == desired_webhook_url:
            self.logger.info(
                "El webhook ya está configurado correctamente en: %s", 
                desired_webhook_url
            )
            return True
        return False

    def configure_webhook(self, public_url):
        "Configura el webhook con la URL proporcionada"
        self.logger.debug("Configurando webhook con la URL pública: %s", public_url)
        success, error = self.telegram_service.configure_webhook(public_url)
        if success:
            self.logger.info("Webhook configurado correctamente en: %s", public_url)
            return True
        self.logger.error("Error configurando webhook: %s", error)
        return False

    def run_configuration(self):
        " Ejecuta el flujo de configuración del webhook "
        public_url = self.get_public_url()
        if not public_url:
            self.logger.error("No se obtuvo una URL pública válida")
            return False
        if self.verify_webhook(public_url):
            return True
        return self.configure_webhook(public_url)
