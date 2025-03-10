"""
Path: src/webhook.py
"""

from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.services.telegram_service import TelegramService
from src.utils.logging.dependency_injection import get_logger

# Initialize logger
logger = get_logger("app_controller")

# Se crea una instancia con una interfaz por defecto (sin colores)
default_interface = Interface(use_colors=False)
presentation_service = PresentationService(default_interface)

def try_configure_webhook(use_colors):
    """Intenta configurar el webhook de Telegram"""
    public_url, error = get_public_url()
    if not public_url:
        print(f"No se pudo obtener la URL pública: {error}")
        return False
    # Inicializar los servicios necesarios
    local_interface = Interface(use_colors=use_colors)  # Usar configuración centralizada
    local_presentation_service = PresentationService(local_interface)
    telegram_service = TelegramService()
    # Configurar el webhook
    success, error_message = configure_webhook(
        base_url=public_url,
        webhook_endpoint="webhook",  # Ajusta esto según tu configuración
        prs=local_presentation_service,
        telegram_service=telegram_service
    )
    if success:
        print("Webhook configurado correctamente")
        return True
    else:
        print(f"Error al configurar webhook: {error_message}")
        return False

def configure_webhook(base_url, webhook_endpoint, prs, telegram_service):
    """Configura el webhook de Telegram

    Args:
        base_url (str): URL base del servidor
        webhook_endpoint (str): Endpoint del webhook
        prs (PresentationService): Servicio de presentación
        telegram_service (TelegramService): Servicio de Telegram

    Returns:
        tuple: (bool, str) - (éxito, mensaje de error)
    """
    prs.notify_operation_start("Configuración de webhook")

    try:
        # Intentar configurar webhook
        webhook_url = f"{base_url}/{webhook_endpoint}"
        prs.show_debug_info(
            f"Intentando configurar webhook en: {webhook_url}"
        )

        success, error_message = telegram_service.configure_webhook(webhook_url)

        if success:
            prs.show_webhook_status(True, webhook_url)
            return True, None
        else:
            prs.show_webhook_status(False)

            # Solicitar confirmación para reintento
            if prs.ask_for_retry("configuración del webhook"):
                return configure_webhook(
                    base_url, webhook_endpoint, prs, telegram_service
                )  # Reintentar recursivamente
            else:
                prs.show_warning_message(
                    "Webhook no configurado por decisión del usuario"
                )
                return False, "Webhook no configurado por decisión del usuario"

    except (ConnectionError, TimeoutError) as e:
        error_message = f"Error de conexión al configurar webhook: {str(e)}"
        prs.show_error_message(error_message)

        # Solicitar confirmación para reintento
        if prs.ask_for_retry("configuración del webhook"):
            return configure_webhook(
                base_url, webhook_endpoint, prs, telegram_service
            )  # Reintentar recursivamente

        return False, error_message
    except ValueError as e:
        error_message = f"Error de valor al configurar webhook: {str(e)}"
        prs.show_error_message(error_message)

        # Solicitar confirmación para reintento
        if prs.ask_for_retry("configuración del webhook"):
            return configure_webhook(
                base_url, webhook_endpoint, prs, telegram_service
            )  # Reintentar recursivamente

        return False, error_message
    except OSError as e:
        error_message = f"Error del sistema al configurar webhook: {str(e)}"
        prs.show_error_message(error_message)

        # Solicitar confirmación para reintento
        if prs.ask_for_retry("configuración del webhook"):
            return configure_webhook(
                base_url, webhook_endpoint, prs, telegram_service
            )  # Reintentar recursivamente

        return False, error_message


def get_public_url():
    " Solicita al usuario la URL pública y la valida "
    try:
        # Usar el servicio de presentación para organización visual y solicitud
        public_url = PresentationService.ask_for_public_url()

        if not public_url:
            error_msg = "No se proporcionó una URL"
            presentation_service.show_message_send_error(error_msg)
            return None, error_msg

        if not public_url.startswith(("http://", "https://")):
            error_msg = "La URL debe comenzar con http:// o https://"
            presentation_service.show_message_send_error(error_msg)
            return None, error_msg

        logger.info("URL proporcionada: %s", public_url)
        return public_url, None

    except KeyboardInterrupt:
        error_msg = "Operación cancelada por el usuario"
        presentation_service.show_message_send_error(error_msg)
        return None, error_msg
    except ValueError as e:
        error_msg = f"Error de valor obteniendo la URL pública: {str(e)}"
        presentation_service.show_message_send_error(error_msg)
        return None, error_msg
    except OSError as e:
        error_msg = f"Error del sistema obteniendo la URL pública: {str(e)}"
        presentation_service.show_message_send_error(error_msg)
        return None, error_msg
