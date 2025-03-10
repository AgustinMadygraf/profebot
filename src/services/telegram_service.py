"""
Path: src/services/telegram_service.py
Servicio para interactuar con la API de Telegram.
Encapsula toda la lógica de comunicación con Telegram.
"""

import os
from typing import Tuple, Dict, Any, Optional
import requests
from src.models.app_model import TelegramUpdate

class TelegramService:
    """Servicio para interactuar con la API de Telegram."""

    @staticmethod
    def validate_token() -> Tuple[bool, Optional[str]]:
        """
        Valida que el token de Telegram esté configurado y tenga un formato básico correcto.
        
        Returns:
            Tuple[bool, Optional[str]]: (éxito, mensaje_error)
        """
        token = os.getenv("TELEGRAM_TOKEN")
        if not token:
            return False, "TELEGRAM_TOKEN no está definido en las variables de entorno"

        # Validar formato básico del token (debe contener :)
        if ":" not in token:
            return False, "TELEGRAM_TOKEN tiene un formato inválido"

        return True, None

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

        token = os.getenv("TELEGRAM_TOKEN")
        set_webhook_url = f"https://api.telegram.org/bot{token}/setWebhook?url={url}"

        try:
            response = requests.get(set_webhook_url, timeout=10)
            response.raise_for_status()
            return True, None
        except requests.exceptions.RequestException as e:
            return False, f"Error configurando webhook: {str(e)}"

    @staticmethod
    def send_message(chat_id: int, text: str) -> Tuple[bool, Optional[str]]:
        """
        Envía un mensaje a un chat de Telegram.
        
        Args:
            chat_id: ID del chat
            text: Texto a enviar
            
        Returns:
            Tuple[bool, Optional[str]]: (éxito, mensaje_error)
        """
        valid, error_msg = TelegramService.validate_token()
        if not valid:
            return False, error_msg

        token = os.getenv("TELEGRAM_TOKEN")
        send_message_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}

        try:
            response = requests.post(send_message_url, json=payload, timeout=10)
            response.raise_for_status()
            return True, None
        except requests.exceptions.RequestException as e:
            return False, f"Error enviando mensaje: {str(e)}"

    @staticmethod
    def parse_update(update: Dict[str, Any]) -> Optional[TelegramUpdate]:
        """
        Parsea un update de Telegram.
        
        Args:
            update: Datos del update de Telegram
            
        Returns:
            Optional[TelegramUpdate]: Objeto parseado o None si hay error
        """
        try:
            return TelegramUpdate.parse_obj(update)
        except ValueError:
            return None

#    def set_webhook(self, webhook_url: str) -> bool:
        # Dummy implementation: simula que el webhook se ha configurado exitosamente.
        # En producción, aquí se realizaría la llamada a la API de Telegram.
        #return True
