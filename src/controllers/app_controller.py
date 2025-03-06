"""
Path: src/controllers/app_controller.py

"""

import os
import requests
from utils.logging.dependency_injection import get_logger

# Initialize logger
logger = get_logger("app_controller")

def validate_telegram_token() -> bool:
    """
    Valida que el token de Telegram esté definido y sea válido.
    
    Returns:
        bool: True si el token es válido, False en caso contrario
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
    Obtiene la URL pública:
      - Primero la busca en la variable de entorno PUBLIC_URL.
      - Si no está definida, solicita al usuario que la ingrese.
    Returns:
        tuple: (url, error_message)
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
    Configura el webhook de Telegram.
    
    Returns:
        tuple: (success, error_message)
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

def process_update(update: dict):
    """
    Procesa el update recibido desde Telegram.
    Por ahora solo se imprime en consola.
    """
    print("Update recibido:", update)
