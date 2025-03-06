"""
Path: src/models/app_model.py

"""

from typing import Optional, Dict, Any
from pydantic import BaseModel

class TelegramUpdate(BaseModel):
    " Modelo para representar un objeto de actualización de Telegram "
    update_id: int
    message: Optional[Dict[str, Any]]
