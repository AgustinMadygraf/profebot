"""
Path: src/controllers/app_controller.py

"""

import os
import requests
from utils.logging.dependency_injection import get_logger
from src.models.app_model import TelegramUpdate
# Importar directamente de interface en lugar de src.cli
from src.cli.interface import info, debug, error, warning, get_input, section

# Initialize logger
logger = get_logger("app_controller")

def validate_telegram_token() -> bool:
    """
    Validates the presence and basic format of the Telegram token.

    Checks if the 'TELEGRAM_TOKEN' environment variable is defined and contains 
    a colon (':') to suggest a valid format.

    Returns:
        bool: True if the token exists and is valid, False otherwise.
    """
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        error("TELEGRAM_TOKEN no está definido en las variables de entorno")
        return False

    # Validar formato básico del token (debe contener :)
    if ":" not in token:
        error("TELEGRAM_TOKEN tiene un formato inválido")
        return False

    return True

def get_public_url():
    " Solicita al usuario la URL pública y la valida "
    try:
        # Usar la nueva función de sección para una mejor organización visual
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

        # Solo logueamos una vez la URL proporcionada
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

    token = os.getenv("TELEGRAM_TOKEN")
    public_url, err = get_public_url()
    if not public_url:
        return False, err

    webhook_url = public_url
    set_webhook_url = f"https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}"

    try:
        response = requests.get(set_webhook_url, timeout=10)
        response.raise_for_status()
        info("Webhook configurado en: %s", webhook_url)
        info("El webhook se ejecutó con éxito.")
        return True, ""
    except requests.exceptions.RequestException as e:
        error_msg = f"Error configurando webhook: {str(e)}"
        error(error_msg)
        return False, error_msg


def parse_update(update: dict) -> TelegramUpdate | None:
    " Parsea un update de Telegram y retorna un objeto TelegramUpdate "
    try:
        return TelegramUpdate.parse_obj(update)
    except ValueError as e:
        error("Error parseando el update: %s", e)
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
    token = os.getenv("TELEGRAM_TOKEN")
    send_message_url = f"https://api.telegram.org/bot{token}/sendMessage"
    debug("Enviando mensaje a URL: %s", send_message_url)
    payload = {"chat_id": chat_id, "text": text}
    debug("Payload: %s", payload)
    try:
        r = requests.post(send_message_url, json=payload, timeout=10)
        r.raise_for_status()
        info("Mensaje enviado a Telegram a chat_id %s", chat_id)
    except requests.exceptions.HTTPError as e:
        error("HTTP error enviando mensaje a Telegram: %s", e)
    except requests.exceptions.ConnectionError as e:
        error("Connection error enviando mensaje a Telegram: %s", e)
    except requests.exceptions.Timeout as e:
        error("Timeout enviando mensaje a Telegram: %s", e)
    except requests.exceptions.RequestException as e:
        error("Error inesperado enviando mensaje a Telegram: %s", e)

def process_update(update: dict) -> str | None:
    " Procesa un update de Telegram y retorna una respuesta si es necesario "
    info("Procesando update: %s", update)
    telegram_update = parse_update(update)
    debug("Update parseado: %s", telegram_update)
    if not telegram_update:
        return None

    response = generate_response(telegram_update)
    if response:
        info("Respuesta generada: %s", response)
        send_message(telegram_update, response)
        return response
    else:
        info("Update recibido sin respuesta generada: %s", update)
        return None
