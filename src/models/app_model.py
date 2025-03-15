"""
Path: src/models/app_model.py
"""

from typing import Optional, Dict, Any, Tuple
from grpc import RpcError
from google.api_core.exceptions import GoogleAPIError
from pydantic import BaseModel
from src.utils.logging.simple_logger import get_logger
from src.services.config_service import get_system_instructions
from src.configuration.central_config import CentralConfig
from src.services.gemini_service import GeminiService
from src.services.telegram_service import TelegramService

_fallback_logger = get_logger()
class TelegramUpdate(BaseModel):
    " Modelo para representar un objeto de actualización de Telegram "
    update_id: int
    message: Optional[Dict[str, Any]]
    def get_response(self) -> Optional[str]:
        " Procesa el mensaje recibido y retorna una respuesta"
        if self.message:
            text = self.message.get('text')
            if text.lower() == 'test':
                return (
                    "¡Hola! ¿Cómo puedo ayudarte? <modo test>."
                )
            api_key = CentralConfig.GEMINI_API_KEY
            if not api_key:
                return "Error: GEMINI_API_KEY no configurado."
            system_instruction = self._load_system_instruction()
            # Utilizar GeminiService en lugar de GeminiLLMClient
            client = GeminiService(api_key, system_instruction)
            try:
                return client.send_message(text)
            except (RpcError, GoogleAPIError) as e:
                return f"Error generando respuesta: {e}"
        return None

    def _load_system_instruction(self) -> str:
        "Carga las instrucciones del sistema desde el servicio de configuración."
        try:
            system_instruction = get_system_instructions()
            _fallback_logger.info(
                "Instrucciones de sistema obtenidas desde DB: %s", 
                system_instruction
            )
            return system_instruction
        except (ConnectionError, TimeoutError, ValueError) as e:
            _fallback_logger.error(
                "Error al cargar instrucciones desde el servicio de configuración: %s", 
                e
            )
            return "Responde de forma amistosa."

    @staticmethod
    def parse_update(update: Dict[str, Any]) -> Optional["TelegramUpdate"]:
        """
        Parsea un diccionario con datos de Telegram y retorna un objeto TelegramUpdate.
        
        Args:
            update: Diccionario con los datos del update.
            
        Returns:
            Optional[TelegramUpdate]: Objeto TelegramUpdate o 
            None si ocurre error o la validación falla.
        """
        try:
            parsed = TelegramUpdate.parse_obj(update)
            # ...existing code... (se elimina la validación externa redundante)
            return parsed
        except ValueError:
            return None

    def send_message(self, text: str) -> Tuple[bool, Optional[str]]:
        " Envía un mensaje a un chat de Telegram "
        if not (self.message and "chat" in self.message and "id" in self.message["chat"]):
            return False, "chat_id no encontrado en el update"
        service = TelegramService()
        return service.send_message(self.message["chat"]["id"], text)

# Eliminamos la definición duplicada del cliente Gemini.
# class GeminiLLMClient(IStreamingLLMClient):
#     """
#     Encapsula la lógica de interacción con el modelo de Gemini,
#     implementando envío de mensajes y streaming.
#     """
#     def __init__(self, api_key: str, system_instruction: str, logger=None):
#         ...existing code...
#     def send_message(self, message: str) -> str:
#         ...existing code...
#     def send_message_streaming(self, message: str, chunk_size: int = 30) -> str:
#         ...existing code...
#     def _start_chat_session(self):
#         ...existing code...
