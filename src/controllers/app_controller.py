"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

from utils.logging.dependency_injection import get_logger
from src.models.app_model import TelegramUpdate
from src.services.telegram_service import TelegramService
from src.services.presentation_service import PresentationService

# Initialize logger
logger = get_logger("app_controller")

def validate_telegram_token() -> bool:
    """
    Validates the presence and basic format of the Telegram token.
    """
    valid, error_msg = TelegramService.validate_token()
    if not valid:
        PresentationService.show_message_send_error(error_msg)
        return False
    return True

def get_public_url():
    " Solicita al usuario la URL pública y la valida "
    try:
        # Usar el servicio de presentación para organización visual y solicitud
        public_url = PresentationService.ask_for_public_url()

        if not public_url:
            error_msg = "No se proporcionó una URL"
            PresentationService.show_message_send_error(error_msg)
            return None, error_msg

        if not public_url.startswith(("http://", "https://")):
            error_msg = "La URL debe comenzar con http:// o https://"
            PresentationService.show_message_send_error(error_msg)
            return None, error_msg

        logger.info("URL proporcionada: %s", public_url)
        return public_url, None

    except KeyboardInterrupt:
        error_msg = "Operación cancelada por el usuario"
        PresentationService.show_message_send_error(error_msg)
        return None, error_msg
    except ValueError as e:
        error_msg = f"Error de valor obteniendo la URL pública: {str(e)}"
        PresentationService.show_message_send_error(error_msg)
        return None, error_msg
    except OSError as e:
        error_msg = f"Error del sistema obteniendo la URL pública: {str(e)}"
        PresentationService.show_message_send_error(error_msg)
        return None, error_msg

def configure_webhook() -> tuple[bool, str]:
    """
    Configures the Telegram webhook with the provided token and public URL.
    """
    if not validate_telegram_token():
        return False, "Token de Telegram inválido o no configurado"

    public_url, err = get_public_url()
    if not public_url:
        return False, err

    success, error_msg = TelegramService.configure_webhook(public_url)

    if success:
        # Replace direct call to info() with PresentationService
        logger.info("Webhook configurado en: %s", public_url)
        PresentationService.show_webhook_configuration_success(public_url)
        return True, ""
    else:
        # Replace direct call to error() with PresentationService
        PresentationService.show_message_send_error(error_msg)
        return False, error_msg

def process_update(update: dict) -> str | None:
    " Procesa un update de Telegram y retorna una respuesta si es necesario "
    logger.info("Procesando update")

    # Usar el servicio de presentación
    PresentationService.show_update_processing(update)

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
        PresentationService.show_response_generated(response)
        send_message(telegram_update, response)
        return response
    else:
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
        PresentationService.show_message_send_error("chat_id no encontrado en el update")
        return

    chat_id = chat["id"]
    logger.debug("Enviando mensaje al chat_id: %s", chat_id)

    # Usar el servicio para enviar el mensaje
    success, error_msg = TelegramService.send_message(chat_id, text)

    if success:
        PresentationService.show_message_sent(chat_id)
    else:
        PresentationService.show_message_send_error(error_msg)
