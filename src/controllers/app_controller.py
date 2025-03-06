"""
Path: src/controllers/app_controller.py

"""

import os
import requests
from utils.logging.dependency_injection import get_logger
from src.models.app_model import TelegramUpdate  # ...nuevo import...

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
        logger.error("TELEGRAM_TOKEN no está definido en las variables de entorno")
        return False

    # Validar formato básico del token (debe contener :)
    if ":" not in token:
        logger.error("TELEGRAM_TOKEN tiene un formato inválido")
        return False

    return True

def get_public_url():
    """
    Retrieves the public URL for the webhook configuration.

    This function first checks the 'PUBLIC_URL' environment variable.
    If not set, it prompts the user to input a temporary public URL.
    It ensures that the URL starts with 'http://' or 'https://'.

    Returns:
        tuple: A tuple containing:
            - str: The retrieved public URL if successful.
            - None if successful, or an error message string upon failure.
    """
    public_url = os.getenv("PUBLIC_URL")
    if public_url:
        logger.info("Usando PUBLIC_URL del entorno: %s", public_url)
        return public_url, None

    try:
        # Solo imprimimos una vez el mensaje
        print("\n=== Configuración de URL Pública ===")
        print("Por favor, ingrese la URL pública temporal del servidor.")
        print("Ejemplo: https://abc123.ngrok.io")
        print("Nota: Asegúrese de incluir 'https://' al inicio\n")

        public_url = input("URL pública: ").strip()

        if not public_url:
            logger.error("No se proporcionó una URL")
            return None, "No se proporcionó una URL"

        if not public_url.startswith(("http://", "https://")):
            logger.error("La URL debe comenzar con http:// o https://")
            return None, "La URL debe comenzar con http:// o https://"

        # Solo logueamos una vez la URL proporcionada
        logger.info("URL proporcionada: %s", public_url)
        return public_url, None

    except KeyboardInterrupt:
        logger.warning("Operación cancelada por el usuario")
        return None, "Operación cancelada por el usuario"
    except ValueError as e:
        error_msg = f"Error de valor obteniendo la URL pública: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
    except OSError as e:
        error_msg = f"Error del sistema obteniendo la URL pública: {str(e)}"
        logger.error(error_msg)
        return None, error_msg

def configure_webhook() -> tuple[bool, str]:
    """
    Configures the Telegram webhook with the provided token and public URL.

    The function performs the following steps:
      1. Validates the Telegram token.
      2. Retrieves the public URL.
      3. Sends a request to Telegram's API to set the webhook.

    Returns:
        tuple: A tuple containing:
            - bool: True if the webhook was successfully configured, False otherwise.
            - str: An empty string on success, or an error message on failure.
    """
    if not validate_telegram_token():
        return False, "Token de Telegram inválido o no configurado"

    token = os.getenv("TELEGRAM_TOKEN")
    public_url, error = get_public_url()
    if not public_url:
        return False, error

    webhook_url = public_url
    set_webhook_url = f"https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}"

    try:
        response = requests.get(set_webhook_url, timeout=10)
        response.raise_for_status()
        # Solo logueamos una vez el éxito
        logger.info("Webhook configurado en: %s", webhook_url)
        return True, ""
    except requests.exceptions.RequestException as e:
        error_msg = f"Error configurando webhook: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def process_update(update: dict) -> str | None:
    """
    Processes the update received from Telegram.

    Currently, this function prints the update to the console.
    Future enhancements might include additional processing logic.

    Args:
        update (dict): The update payload received from Telegram.
    """
    # Convertir el diccionario update en un objeto TelegramUpdate
    try:
        telegram_update = TelegramUpdate.parse_obj(update)
    except Exception as e:
        print("Error parseando el update:", e)
        return None

    response = telegram_update.get_response()
    if response:
        print("Respuesta generada:", response)
        # Enviar el mensaje generado a través de Telegram
        chat = telegram_update.message.get("chat") if telegram_update.message else None
        if chat and "id" in chat:
            chat_id = chat["id"]
            token = os.getenv("TELEGRAM_TOKEN")
            send_message_url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": response}
            try:
                r = requests.post(send_message_url, json=payload, timeout=10)
                r.raise_for_status()
                print("Mensaje enviado a Telegram.")
            except requests.exceptions.RequestException as e:
                print("Error enviando mensaje a Telegram:", e)
        else:
            print("chat_id no encontrado en el update.")
        return response
    else:
        print("Update recibido:", update)
        return None
