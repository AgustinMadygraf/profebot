"""
Path: src/interfaces/messaging_service.py
"""

__all__ = ["IMessagingService"]

from abc import ABC, abstractmethod
from typing import Tuple, Optional

class IMessagingService(ABC):
    "Interfaz para un servicio de mensajería"
    @abstractmethod
    def send_message(self, chat_id: int, text: str) -> Tuple[bool, Optional[str]]:
        "Envía un mensaje a un chat de Telegram"
        raise NotImplementedError
