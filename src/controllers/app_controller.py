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

def configure_webhook(base_url, webhook_endpoint, presentation_service, telegram_service):
    """Configura el webhook de Telegram
    
    Args:
        base_url (str): URL base del servidor
        webhook_endpoint (str): Endpoint del webhook
        presentation_service (PresentationService): Servicio de presentación
        telegram_service (TelegramService): Servicio de Telegram
        
    Returns:
        tuple: (bool, str) - (éxito, mensaje de error)
    """
    presentation_service.notify_operation_start("Configuración de webhook")

    try:
        # Intentar configurar webhook
        webhook_url = f"{base_url}/{webhook_endpoint}"
        presentation_service.show_debug_info(
            f"Intentando configurar webhook en: {webhook_url}"
        )

        success, error_message = telegram_service.configure_webhook(webhook_url)

        if success:
            presentation_service.show_webhook_status(True, webhook_url)
            return True, None
        else:
            presentation_service.show_webhook_status(False)

            # Solicitar confirmación para reintento
            if presentation_service.ask_for_retry("configuración del webhook"):
                return configure_webhook(
                    base_url, webhook_endpoint, presentation_service, telegram_service
                )  # Reintentar recursivamente
            else:
                presentation_service.show_warning_message(
                    "Webhook no configurado por decisión del usuario"
                )
                return False, "Webhook no configurado por decisión del usuario"

    except (ConnectionError, TimeoutError) as e:
        error_message = f"Error de conexión al configurar webhook: {str(e)}"
        presentation_service.show_error_message(error_message)

        # Solicitar confirmación para reintento
        if presentation_service.ask_for_retry("configuración del webhook"):
            return configure_webhook(
                base_url, webhook_endpoint, presentation_service, telegram_service
            )  # Reintentar recursivamente

        return False, error_message
    except ValueError as e:
        error_message = f"Error de valor al configurar webhook: {str(e)}"
        presentation_service.show_error_message(error_message)

        # Solicitar confirmación para reintento
        if presentation_service.ask_for_retry("configuración del webhook"):
            return configure_webhook(
                base_url, webhook_endpoint, presentation_service, telegram_service
            )  # Reintentar recursivamente

        return False, error_message
    except OSError as e:
        error_message = f"Error del sistema al configurar webhook: {str(e)}"
        presentation_service.show_error_message(error_message)

        # Solicitar confirmación para reintento
        if presentation_service.ask_for_retry("configuración del webhook"):
            return configure_webhook(
                base_url, webhook_endpoint, presentation_service, telegram_service
            )  # Reintentar recursivamente

        return False, error_message

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
