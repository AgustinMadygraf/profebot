"""
Path: src/models/telegram_update.py

Actualización de validación:
- Se ha implementado validación adicional para asegurar la existencia del campo 'message'
  y de 'message.chat.id' en el update de Telegram.
- Esta mejora aumenta la robustez y evita errores en la cadena de procesamiento.
  
Nota: Revisar ejemplos de datos correctos e incorrectos para futuros mantenimientos.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


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
            return text
        return None

    @staticmethod
    def parse_update(update: Dict[str, Any], logger=None) -> Optional["TelegramUpdate"]:
        "Parsea un objeto de actualización de Telegram con validación adicional"
        try:
            parsed = TelegramUpdate.parse_obj(update)
            # Validación adicional: se requiere el campo 'message' y 'message.chat.id'
            if not parsed.message:
                if logger:
                    logger.warning("Telegram update missing 'message' field: %s", update)
                return None
            if "chat" not in parsed.message or "id" not in parsed.message["chat"]:
                if logger:
                    logger.error("Telegram update missing 'chat.id' field: %s", update)
                return None
            return parsed
        except ValueError as e:
            if logger:
                logger.error("Error parsing Telegram update: %s. Error: %s", update, e)
            return None
