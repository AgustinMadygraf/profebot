"""
Path: src/services/message_sender.py
"""

import os
from typing import Tuple, Optional
import requests
from src.utils.logging.simple_logger import get_logger

logger = get_logger()

def send_message(telegram_update, text: str) -> Tuple[bool, Optional[str]]:
    " Envía un mensaje a un chat de Telegram "
    chat = telegram_update.message.get("chat") if telegram_update.message else None
    if not (chat and "id" in chat):
        return False, "chat_id no encontrado en el update"

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        return False, "TELEGRAM_TOKEN no definido en las variables de entorno"

    send_message_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat["id"], "text": text}
    try:
        response = requests.post(send_message_url, json=payload, timeout=10)
        response.raise_for_status()
        return True, None
    except requests.exceptions.RequestException as e:
        logger.exception("Error enviando mensaje:")
        return False, f"Error enviando mensaje: {str(e)}"
