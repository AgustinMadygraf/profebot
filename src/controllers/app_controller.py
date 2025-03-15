"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

from typing import Optional
from src.utils.logging.simple_logger import get_logger
from src.models.app_model import TelegramUpdate
from src.services.message_sender import send_message as send_msg

# Initialize logger
logger = get_logger()

def process_update(update: dict) -> Optional[str]:
    " Procesa un update de Telegram y genera una respuesta "
    try:
        logger.info("Procesando update")
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
    except (ValueError, KeyError) as e:
        logger.exception("Excepción en process_update: %s", e)
        _handle_error("Error inesperado al procesar el update")
        return None

def _handle_error(message: str) -> None:
    logger.error("Error: %s", message)

def generate_response(telegram_update: TelegramUpdate) -> Optional[str]:
    " Genera una respuesta para un objeto TelegramUpdate "
    return telegram_update.get_response()

def send_message(telegram_update: TelegramUpdate, text: str) -> None:
    " Envía un mensaje a un chat de Telegram "
    success, error_msg = send_msg(telegram_update, text)
    if success:
        logger.info("Mensaje enviado correctamente al chat_id: %s",
                    telegram_update.message.get("chat", {}).get("id"))
    else:
        _handle_error(error_msg)
