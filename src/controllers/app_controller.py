"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""
from typing import Optional
from src.utils.logging.simple_logger import get_logger
from src.models.app_model import TelegramUpdate
from src.services.telegram_service import TelegramService

# Initialize logger
logger = get_logger()

def process_update(update: dict) -> Optional[str]:
    " Procesa un update de Telegram y genera una respuesta "
    try:
        logger.info("Procesando update")
        telegram_update = TelegramUpdate.parse_update(update)
        logger.debug("Update parseado: %s", telegram_update)

        if not telegram_update:
            logger.error("No se pudo parsear el update")
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
        logger.error("Error inesperado al procesar el update")
        return None

def generate_response(telegram_update: TelegramUpdate) -> Optional[str]:
    " Genera una respuesta para un objeto TelegramUpdate "
    return telegram_update.get_response()

def send_message(telegram_update: TelegramUpdate, text: str) -> None:
    "Envía un mensaje a un chat de Telegram usando TelegramService"
    if not (telegram_update.message and
            "chat" in telegram_update.message and 
            "id" in telegram_update.message["chat"]):
        logger.error("chat_id no encontrado en el update")
        return
    service = TelegramService()
    success, error_msg = service.send_message(telegram_update.message["chat"]["id"], text)
    if success:
        chat_id = telegram_update.message["chat"]["id"]
        logger.info("Mensaje enviado correctamente al chat_id: %s", chat_id)
    else:
        logger.error("Error enviando mensaje: %s", error_msg)
