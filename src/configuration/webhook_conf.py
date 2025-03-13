"""
Path: src/configuration/webhook_conf.py
"""

import requests
from src.services.telegram_service import TelegramService
from src.utils.logging.simple_logger import get_logger

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
        """
        Intenta configurar el webhook obteniendo primero la URL de ngrok,
        y en caso de fallo, solicitándola al usuario.
        Antes de configurar, verifica si el webhook ya está correctamente configurado
        para evitar reconfiguraciones innecesarias.
        """
        self.logger.info("Intentando obtener la URL de ngrok desde http://127.0.0.1:4040/")
        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
            data = response.json()
            public_url = None
            tunnels = data.get("tunnels", [])
            if tunnels:
                # Se toma la primera URL válida encontrada en la lista de túneles
                for tunnel in tunnels:
                    if "public_url" in tunnel:
                        public_url = tunnel["public_url"]
                        break
            if public_url:
                self.logger.debug("URL de ngrok obtenida: %s", public_url)
            else:
                self.logger.warning("No se encontró URL de ngrok válida")
                raise RuntimeError("URL de ngrok no encontrada")
        except requests.exceptions.RequestException as e:
            self.logger.debug("Error al obtener URL de ngrok: %s", e)
            public_url, _ = self.get_public_url()
            if not public_url:
                self.logger.error("No se proporcionó una URL válida para configurar el webhook")
                return False

        # Construir la URL deseada para el webhook
        desired_webhook_url = f"{public_url}/webhook"
        self.logger.debug("Verificando configuración actual del webhook...")
        success, info = self.telegram_service.get_webhook_info()
        if success and info.get("result"):
            current_url = info["result"].get("url", "")
            if current_url == desired_webhook_url:
                self.logger.info(
                    "El webhook ya está configurado correctamente en: %s", 
                    desired_webhook_url
                )
                return True
        self.logger.debug("Webhook no configurado o URL diferente. Procediendo a configurar...")
        success, _ = self.configure_webhook(public_url)
        return success
