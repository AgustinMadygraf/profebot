"""
Path: src/services/messaging_base_service.py
"""

__all__ = ["MessagingServiceBase"]

from abc import ABC, abstractmethod

class MessagingServiceBase(ABC):
    """
    Clase base para integración con APIs de mensajería.
    Define métodos comunes para validación, configuración de webhook,
    obtención de información y envío de mensajes.
    """

    @abstractmethod
    def validate_token(self) -> tuple:
        " Método para validar el token de autenticación con la API de mensajería. "
        pass

    @abstractmethod
    def configure_webhook(self, url: str) -> tuple:
        " Método para configurar el webhook de la API de mensajería. "
        pass

    @abstractmethod
    def get_webhook_info(self) -> tuple:
        " Método para obtener información del webhook de la API de mensajería. "
        pass

    @abstractmethod
    def send_message(self, chat_id: int, text: str) -> tuple:
        " Método para enviar un mensaje a un chat de la API de mensajería. "
        pass
