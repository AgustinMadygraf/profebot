"""
Path: src/models/app_model.py

"""

from typing import Optional, Dict, Any
from pydantic import BaseModel

class TelegramUpdate(BaseModel):
    " Modelo para representar un objeto de actualización de Telegram "
    update_id: int
    message: Optional[Dict[str, Any]]

    def get_response(self) -> Optional[str]:
        # Si se recibe un mensaje "test", retorna una respuesta genérica
        if self.message and self.message.get('text') == 'test':
            return "Esta es una respuesta genérica."
        return None
