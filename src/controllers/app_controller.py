"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

from typing import Optional
from src.utils.logging.simple_logger import get_logger
from src.models.app_model import TelegramUpdate
from src.services.telegram_service import TelegramService

logger = get_logger()

class AppController:
    "Controlador de la aplicación que maneja las solicitudes."
    def __init__(self, telegram_service: TelegramService):
        self.logger = logger
        self.telegram_service = telegram_service

    def process_update(self, update: dict) -> Optional[str]:
        "Procesa un update de Telegram y genera una respuesta"
        try:
            self.logger.info("Procesando update")
            telegram_update = TelegramUpdate.parse_update(update)
            self.logger.debug("Update parseado: %s", telegram_update)
            if not telegram_update:
                self.logger.error("No se pudo parsear el update")
                return None

            response = self.generate_response(telegram_update)
            if response:
                self.logger.info("Respuesta generada")
                self.send_message(telegram_update, response)
                return response

            self.logger.info("Update recibido sin respuesta generada")
            return None
        except (ValueError, KeyError) as e:
            self.logger.exception("Excepción en process_update: %s", e)
            self.logger.error("Error inesperado al procesar el update")
            return None

    def generate_response(self, telegram_update: TelegramUpdate) -> Optional[str]:
        "Genera una respuesta para un objeto TelegramUpdate"
        return telegram_update.get_response()

    def send_message(self, telegram_update: TelegramUpdate, text: str) -> None:
        "Envía un mensaje a un chat de Telegram usando la instancia inyectada de TelegramService"
        if not (telegram_update.message and
                "chat" in telegram_update.message and 
                "id" in telegram_update.message["chat"]):
            self.logger.error("chat_id no encontrado en el update")
            return

        success, error_msg = self.telegram_service.send_message(
            telegram_update.message["chat"]["id"], text
        )
        if success:
            chat_id = telegram_update.message["chat"]["id"]
            self.logger.info("Mensaje enviado correctamente al chat_id: %s", chat_id)
        else:
            self.logger.error("Error enviando mensaje: %s", error_msg)
