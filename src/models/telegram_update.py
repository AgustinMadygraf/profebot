"""
Path: src/models/telegram_update.py
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel
from src.utils.logging.simple_logger import get_logger

_fallback_logger = get_logger()

# [ANÁLISIS] Clase TelegramUpdate:
# Esta clase se encarga de la validación y representación del update de Telegram.
# Nota: La lógica de comunicación externa (como el envío de mensajes mediante GeminiService)
# debería migrarse a la capa de servicios.
class TelegramUpdate(BaseModel):
    " Modelo para representar un objeto de actualización de Telegram "
    update_id: int
    message: Optional[Dict[str, Any]]
    def get_response(self) -> Optional[str]:
        """
        Procesa el mensaje recibido.
        Si es 'test' retorna el mensaje de prueba;
        de lo contrario, solo retorna el texto para que el controlador invoque al servicio Gemini.
        """
        if self.message:
            text = self.message.get('text')
            if text.lower() == 'test':
                return "¡Hola! ¿Cómo puedo ayudarte? <modo test>."
            # Se elimina la lógica de comunicación externa
            return text
        return None

    @staticmethod
    def parse_update(update: Dict[str, Any]) -> Optional["TelegramUpdate"]:
        " Parsea un objeto de actualización de Telegram "
        try:
            parsed = TelegramUpdate.parse_obj(update)
            return parsed
        except ValueError as e:
            _fallback_logger.error("Error parsing Telegram update: %s. Error: %s", update, e)
            return None
