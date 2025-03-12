"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

import os
import sys
# Agregar el directorio padre para que 'src' sea importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.utils.logging.dependency_injection import get_logger
from src.models.app_model import TelegramUpdate
from src.services.telegram_service import TelegramService
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface

# Initialize logger
logger = get_logger("app_controller")

# Se crea una instancia con una interfaz por defecto (sin colores)
default_interface = Interface(use_colors=False)
presentation_service = PresentationService(default_interface)

def validate_telegram_token() -> bool:
    """
    Validates the presence and basic format of the Telegram token.
    """
    valid, error_msg = TelegramService.validate_token()
    if not valid:
        presentation_service.show_message_send_error(error_msg)
        return False
    return True

def process_update(update: dict) -> str | None:
    " Procesa un update de Telegram y retorna una respuesta si es necesario "
    logger.info("Procesando update")

    # Usar el servicio de presentación
    presentation_service.show_update_processing(update)

    # Usar el servicio para parsear el update
    telegram_update = TelegramService.parse_update(update)
    logger.debug("Update parseado: %s", telegram_update)

    if not telegram_update:
        logger.error("No se pudo parsear el update")
        return None

    # Generar respuesta
    response = generate_response(telegram_update)

    if response:
        logger.info("Respuesta generada")
        presentation_service.show_response_generated(response)
        send_message(telegram_update, response)
        return response

    logger.info("Update recibido sin respuesta generada")
    return None

def generate_response(telegram_update: TelegramUpdate) -> str | None:
    " Genera una respuesta para un objeto TelegramUpdate "
    return telegram_update.get_response()

def send_message(telegram_update: TelegramUpdate, text: str) -> None:
    " Envía un mensaje de texto a un chat de Telegram "
    chat = telegram_update.message.get("chat") if telegram_update.message else None
    if not (chat and "id" in chat):
        logger.error("chat_id no encontrado en el update.")
        presentation_service.show_message_send_error("chat_id no encontrado en el update")
        return

    chat_id = chat["id"]
    logger.debug("Enviando mensaje al chat_id: %s", chat_id)

    # Usar el servicio para enviar el mensaje
    success, error_msg = TelegramService.send_message(chat_id, text)

    if success:
        presentation_service.show_message_sent(chat_id)
    else:
        presentation_service.show_message_send_error(error_msg)
