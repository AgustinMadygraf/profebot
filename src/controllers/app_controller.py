"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

from typing import Optional
from src.models.telegram_update import TelegramUpdate
from src.services.gemini_service import GeminiService
from src.interfaces.messaging_service import IMessagingService

class AppController:
    "Controlador de la aplicación que maneja las solicitudes."
    def __init__(self,
                 messaging_service: IMessagingService,
                 gemini_service: GeminiService,
                 logger=None):
        self.logger = logger
        self.messaging_service = messaging_service
        self.gemini_service = gemini_service

    def process_update(self, update: dict) -> Optional[str]:
        "Procesa un update de Telegram y genera una respuesta"
        try:
            self.logger.info("[AppController] Procesando update")
            telegram_update = TelegramUpdate.parse_update(update, self.logger)
            self.logger.debug("[AppController] Update parseado: %s", telegram_update)
            if not telegram_update:
                self.logger.error("[AppController] No se pudo parsear el update")
                return None

            response = self.generate_response(telegram_update)
            if response:
                self.logger.info("[AppController] Respuesta generada")
                self.send_message(telegram_update, response)
                return response

            self.logger.info("[AppController] Update recibido sin respuesta generada")
            return None
        except (ValueError, KeyError) as e:
            self.logger.exception("[AppController] Excepción en process_update: %s", e)
            self.logger.error("[AppController] Error inesperado al procesar el update")
            return None

    def generate_response(self, telegram_update: TelegramUpdate) -> Optional[str]:
        "Genera una respuesta para un objeto TelegramUpdate utilizando el servicio Gemini."
        original_text = telegram_update.get_response()
        if original_text:
            if original_text.lower() == 'test':
                return original_text
            try:
                response = self.gemini_service.send_message(original_text)
                return response
            except (ConnectionError, TimeoutError) as e:
                self.logger.error(
                    "[AppController] Error de conexión generando respuesta de Gemini: %s", e
                )
                return None
            except ValueError as e:
                self.logger.error(
                    "[AppController] Error de valor generando respuesta de Gemini: %s", e
                )
                return None
        return None

    def send_message(self, telegram_update: TelegramUpdate, text: str) -> None:
        "Envía un mensaje a un chat de Telegram usando la instancia inyectada de TelegramService"
        if not (telegram_update.message and
                "chat" in telegram_update.message and 
                "id" in telegram_update.message["chat"]):
            self.logger.error("[AppController] chat_id no encontrado en el update")
            return

        success, error_msg = self.messaging_service.send_message(
            telegram_update.message["chat"]["id"], text
        )
        if success:
            chat_id = telegram_update.message["chat"]["id"]
            self.logger.info(
                "[AppController] Mensaje enviado correctamente al chat_id: %s", chat_id
            )
        else:
            self.logger.error(
                "[AppController] Error enviando mensaje al chat_id %s, text length %d: %s",
                telegram_update.message["chat"]["id"], len(text), error_msg
            )
