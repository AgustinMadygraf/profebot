"""
Path: src/services/telegram_service.py
Servicio para interactuar con la API de Telegram.
Encapsula toda la lógica de comunicación con Telegram.
"""

from typing import Tuple, Any, Optional
import requests
from src.configuration.central_config import CentralConfig
from src.utils.validation_utils import validate_telegram_token

class TelegramService:
    """Servicio para interactuar con la API de Telegram."""

    @staticmethod
    def validate_token() -> Tuple[bool, Optional[str]]:
        """
        Valida que el token de Telegram esté configurado y tenga el formato adecuado.

        Se delega en la función validate_telegram_token de src/utils/validation_utils.py
        para centralizar la validación.
        """
        return validate_telegram_token()

    @staticmethod
    def configure_webhook(url: str) -> Tuple[bool, Optional[str]]:
        """
        Configura el webhook de Telegram.
        
        Args:
            url: URL pública para el webhook
            
        Returns:
            Tuple[bool, Optional[str]]: (éxito, mensaje_error)
        """
        valid, error_msg = TelegramService.validate_token()
        if not valid:
            return False, error_msg

        token = CentralConfig.TELEGRAM_TOKEN
        set_webhook_url = f"https://api.telegram.org/bot{token}/setWebhook?url={url}"

        try:
            response = requests.get(set_webhook_url, timeout=10)
            response.raise_for_status()
            return True, None
        except requests.exceptions.RequestException as e:
            return False, f"Error configurando webhook: {str(e)}"

    @staticmethod
    def get_webhook_info() -> Tuple[bool, Any]:
        """
        Obtiene información del webhook de Telegram.
        
        Returns:
            Tuple[bool, Any]: (éxito, datos_json_o_mensaje_error)
        """
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
