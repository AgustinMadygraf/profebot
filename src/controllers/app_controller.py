"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

from typing import Optional
from src.utils.logging.simple_logger import get_logger
from src.models.app_model import TelegramUpdate

# Initialize logger
logger = get_logger()

def process_update(update: dict) -> Optional[str]:
    " Procesa un update de Telegram y retorna una respuesta si es necesario "
    logger.info("Procesando update")

    # Se actualiza para usar el método parse_update de TelegramUpdate
    telegram_update = TelegramUpdate.parse_update(update)
    logger.debug("Update parseado: %s", telegram_update)

    if not telegram_update:
        _handle_error("No se pudo parsear el update")
        return None
    response = generate_response(telegram_update)

    if response:
        logger.info("Respuesta generada")
        send_message(telegram_update, response)
        return response

    logger.info("Update recibido sin respuesta generada")
    return None

def _handle_error(message: str) -> None:
    logger.error("Error: %s", message)

def generate_response(telegram_update: TelegramUpdate) -> Optional[str]:
    " Genera una respuesta para un objeto TelegramUpdate "
    return telegram_update.get_response()

def send_message(telegram_update: TelegramUpdate, text: str) -> None:
    " Envía un mensaje de texto a un chat de Telegram "
    chat = telegram_update.message.get("chat") if telegram_update.message else None
    if not (chat and "id" in chat):
        _handle_error("chat_id no encontrado en el update.")
        return

    chat_id = chat["id"]
    logger.debug("Enviando mensaje al chat_id: %s", chat_id)

    # Se actualiza para usar el método de instancia send_message() de TelegramUpdate
    success, error_msg = telegram_update.send_message(text)

    if success:
        chat_id = telegram_update.message.get("chat", {}).get("id")
        logger.info("Mensaje enviado correctamente al chat_id: %s", chat_id)
    else:
        _handle_error(error_msg)
