"""
Path: src/utils/validation_utils.py
"""

from typing import Tuple, Optional
from src.configuration.central_config import CentralConfig

def validate_telegram_token() -> Tuple[bool, Optional[str]]:
    """
    Valida que el token de Telegram esté definido y tenga el formato adecuado.
    """
    token = CentralConfig.TELEGRAM_TOKEN
    if not token:
        return False, "TELEGRAM_TOKEN no está definido en las variables de entorno"
    if ":" not in token:
        return False, "TELEGRAM_TOKEN tiene un formato inválido"
    return True, None
