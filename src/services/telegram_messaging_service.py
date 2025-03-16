"""
Path: src/services/telegram_messaging_service.py
"""

from typing import Tuple, Optional, Any
from src.interfaces.messaging_service import IMessagingService
from src.services.telegram_service import TelegramService

class TelegramMessagingService(IMessagingService):
    "Servicio para enviar mensajes a través"
    def __init__(self):
        self._telegram_service = TelegramService()

    def send_message(self, chat_id: int, text: str) -> Tuple[bool, Optional[str]]:
        "Envía un mensaje a un chat de Telegram"
        return self._telegram_service.send_message(chat_id, text)

    def get_webhook_info(self) -> Tuple[bool, Any]:
        "Obtiene información del webhook delegando a TelegramService"
        return self._telegram_service.get_webhook_info()

    def configure_webhook(self, url: str) -> Tuple[bool, Optional[str]]:
        "Configura el webhook delegando a TelegramService"
        return self._telegram_service.configure_webhook(url)
