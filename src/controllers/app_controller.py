"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""
from src.utils.logging.simple_logger import get_logger
from src.models.app_model import TelegramUpdate
from src.services.telegram_service import TelegramService
from typing import Optional  # Import Optional from typing

# Initialize logger
logger = get_logger()


def _handle_error(message: str) -> None:
    logger.error("Error: %s", message)

def validate_telegram_token() -> bool:
    """
    Validates the presence and basic format of the Telegram token.
    """
    valid, error_msg = TelegramService.validate_token()
    if not valid:
        _handle_error(error_msg)
        return False
    return True

def process_update(update: dict) -> Optional[str]:
    " Procesa un update de Telegram y retorna una respuesta si es necesario "
    logger.info("Procesando update")

    telegram_update = TelegramService.parse_update(update)
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

    success, error_msg = TelegramService.send_message(chat_id, text)

    if success:
        logger.info("Mensaje enviado correctamente al chat_id: %s", chat_id)
    else:
        _handle_error(error_msg)
