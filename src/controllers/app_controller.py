"""
Path: src/controllers/app_controller.py
Controlador de la aplicación que maneja las solicitudes.
"""

from utils.logging.dependency_injection import get_logger
from src.models.app_model import TelegramUpdate
from src.cli.interface import info, debug, error, warning, get_input, section
from src.services.telegram_service import TelegramService

# Initialize logger
logger = get_logger("app_controller")

def validate_telegram_token() -> bool:
    """
    Validates the presence and basic format of the Telegram token.
    """
    valid, error_msg = TelegramService.validate_token()
    if not valid:
        error(error_msg)
        return False
    return True

def get_public_url():
    " Solicita al usuario la URL pública y la valida "
    try:
        # Mejor organización visual
        section("Configuración de URL Pública")
        info("Por favor, ingrese la URL pública temporal del servidor.")
        info("Ejemplo: https://abc123.ngrok.io")
        info("Nota: Asegúrese de incluir 'https://' al inicio")

        public_url = get_input("URL pública: ").strip()

        if not public_url:
            error("No se proporcionó una URL")
            return None, "No se proporcionó una URL"

        if not public_url.startswith(("http://", "https://")):
            error("La URL debe comenzar con http:// o https://")
            return None, "La URL debe comenzar con http:// o https://"

        info("URL proporcionada: %s", public_url)
        return public_url, None

    except KeyboardInterrupt:
        warning("Operación cancelada por el usuario")
        return None, "Operación cancelada por el usuario"
    except ValueError as e:
        error_msg = f"Error de valor obteniendo la URL pública: {str(e)}"
        error(error_msg)
        return None, error_msg
    except OSError as e:
        error_msg = f"Error del sistema obteniendo la URL pública: {str(e)}"
        error(error_msg)
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
        info("Webhook configurado en: %s", public_url)
        info("El webhook se ejecutó con éxito.")
        return True, ""
    else:
        error(error_msg)
        return False, error_msg

def process_update(update: dict) -> str | None:
    " Procesa un update de Telegram y retorna una respuesta si es necesario "
    info("Procesando update: %s", update)

    # Usar el servicio para parsear el update
    telegram_update = TelegramService.parse_update(update)
    debug("Update parseado: %s", telegram_update)

    if not telegram_update:
        error("No se pudo parsear el update")
        return None

    # Generar respuesta
    response = generate_response(telegram_update)

    if response:
        info("Respuesta generada: %s", response)
        send_message(telegram_update, response)
        return response
    else:
        info("Update recibido sin respuesta generada")
        return None

def generate_response(telegram_update: TelegramUpdate) -> str | None:
    " Genera una respuesta para un objeto TelegramUpdate "
    return telegram_update.get_response()

def send_message(telegram_update: TelegramUpdate, text: str) -> None:
    " Envía un mensaje de texto a un chat de Telegram "
    chat = telegram_update.message.get("chat") if telegram_update.message else None
    if not (chat and "id" in chat):
        error("chat_id no encontrado en el update.")
        return

    chat_id = chat["id"]
    debug("Enviando mensaje al chat_id: %s", chat_id)

    # Usar el servicio para enviar el mensaje
    success, error_msg = TelegramService.send_message(chat_id, text)

    if success:
        info("Mensaje enviado a Telegram a chat_id %s", chat_id)
    else:
        error(error_msg)
