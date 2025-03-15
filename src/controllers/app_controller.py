"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""
from typing import Tuple, Optional
import requests
from src.utils.logging.simple_logger import get_logger
from src.models.app_model import TelegramUpdate
import src.configuration.central_config as central_config

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
    " Envía un mensaje a un chat de Telegram "
    success, error_msg = send_msg(telegram_update, text)
    if success:
        logger.info("Mensaje enviado correctamente al chat_id: %s",
                    telegram_update.message.get("chat", {}).get("id"))
    else:
        logger.error("Error enviando mensaje: %s", error_msg)

def send_msg(telegram_update, text: str) -> Tuple[bool, Optional[str]]:
    " Envía un mensaje a un chat de Telegram "
    chat = telegram_update.message.get("chat") if telegram_update.message else None
    if not (chat and "id" in chat):
        return False, "chat_id no encontrado en el update"

    token = central_config.CentralConfig.TELEGRAM_TOKEN
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
