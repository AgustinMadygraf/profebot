"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

from typing import Optional
from src.utils.logging.simple_logger import get_logger
from src.models.app_model import TelegramUpdate
from src.services.telegram_service import TelegramService

class AppController:
    " Controlador de la aplicación que maneja las solicitudes. "
    def __init__(self):
        self.logger = get_logger()

    def process_update(self, update: dict) -> Optional[str]:
        " Procesa un update de Telegram y retorna una respuesta. "
        self.logger.info("Procesando update")
        self.logger.debug("Iniciando procesamiento del update con historial de conversación activo")
        telegram_update = TelegramUpdate.parse_update(update)
        self.logger.debug("Update parseado: %s", telegram_update)
        if not telegram_update:
            self.logger.error("No se pudo parsear el update")
            return None
        response = self.generate_response(telegram_update)
        self.logger.debug("Respuesta generada: %s", response)
        if response:
            self.send_message(telegram_update, response)
            self.logger.debug("Historial de conversación actualizado tras enviar respuesta")
            return response
        self.logger.info("Update recibido sin respuesta generada")
        return None

    def generate_response(self, telegram_update: TelegramUpdate) -> Optional[str]:
        " Genera una respuesta a partir de un update de Telegram. "
        return telegram_update.get_response()

    def send_message(self, telegram_update: TelegramUpdate, text: str) -> None:
        " Envía un mensaje a un chat de Telegram. "
        if not (
            telegram_update.message and
            "chat" in telegram_update.message and 
            "id" in telegram_update.message["chat"]
        ):
            self.logger.error("chat_id no encontrado en el update")
            return
        service = TelegramService()
        success, error_msg = service.send_message(telegram_update.message["chat"]["id"], text)
        if success:
            chat_id = telegram_update.message["chat"]["id"]
            self.logger.info("Mensaje enviado correctamente al chat_id: %s", chat_id)
        else:
            self.logger.error("Error enviando mensaje: %s", error_msg)
