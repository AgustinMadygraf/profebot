"""
Path: src/utils/error_handler.py
"""

import traceback
from src.utils.config.app_config import get_config
from src.utils.message_formatter import format_message  # Nuevo import

def log_error(presentation_service, logger, message, error):
    "Registra y notifica el error de forma unificada"
    full_message = format_message("error", f"{message}: {error}")
    presentation_service.notify("error", full_message)
    logger.error(full_message)

def log_warning(presentation_service, logger, message, warning):
    "Registra y notifica la advertencia de forma unificada"
    full_message = format_message("warning", f"{message}: {warning}")
    presentation_service.notify("warning", full_message)
    logger.warning(full_message)

def log_info(presentation_service, logger, message):
    "Registra y muestra un mensaje informativo unificado"
    full_message = format_message("info", message)
    presentation_service.notify("info", full_message)
    logger.info(full_message)

def log_exception(presentation_service, logger, message, exception):
    "Registra y notifica la excepción completa de manera unificada"
    config = get_config()
    full_message = f"{message}: {exception}"
    if config.get("verbose_mode"):
        tb = traceback.format_exc()
        full_message += f"\nTraceback:\n{tb}"
    full_message = format_message("error", full_message)
    presentation_service.notify("error", full_message)
    logger.exception(full_message)
