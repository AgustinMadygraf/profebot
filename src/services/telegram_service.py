"""
Path: src/services/telegram_service.py
Servicio para interactuar con la API de Telegram.
Encapsula toda la lógica de comunicación con Telegram.
"""

from typing import Tuple, Any, Optional
import requests
from src.configuration.central_config import CentralConfig

class TelegramService:
    "Servicio para interactuar con la API de Telegram."
    @staticmethod
    def validate_token() -> Tuple[bool, Optional[str]]:
        " Valida que el token de Telegram esté definido y tenga un formato válido."
        token = CentralConfig.TELEGRAM_TOKEN
        if not token:
            return False, "TELEGRAM_TOKEN no está definido en las variables de entorno"
        if ":" not in token:
            return False, "TELEGRAM_TOKEN tiene un formato inválido"
        return True, None

    @staticmethod
    def get_webhook_info() -> Tuple[bool, Any]:
        " Obtiene información del webhook configurado en Telegram."
        valid, error_msg = TelegramService.validate_token()
        if not valid:
            return False, error_msg

        token = CentralConfig.TELEGRAM_TOKEN
        webhook_info_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"

        try:
            response = requests.get(webhook_info_url, timeout=10)
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            return False, f"Error obteniendo información del webhook: {str(e)}"

    def send_message(self, chat_id: int, text: str) -> Tuple[bool, Optional[str]]:
        " Envía un mensaje de texto a un chat de Telegram."
        token = CentralConfig.TELEGRAM_TOKEN
        if not token:
            return False, "TELEGRAM_TOKEN no definido"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True, None
        except requests.exceptions.RequestException as e:
            return False, f"Error enviando mensaje: {e}"
