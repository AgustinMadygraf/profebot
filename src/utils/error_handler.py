"""
Path: src/utils/error_handler.py
"""

def log_error(presentation_service, logger, message, error):
    "Registra y notifica el error de forma unificada"
    full_message = f"{message}: {error}"
    presentation_service.notify("error", full_message)
    logger.error(full_message)

def log_warning(presentation_service, logger, message, warning):
    "Registra y notifica la advertencia de forma unificada"
    full_message = f"{message}: {warning}"
    presentation_service.notify("warning", full_message)
    logger.warning(full_message)

def log_info(presentation_service, logger, message):
    "Registra y muestra un mensaje informativo unificado"
    presentation_service.notify("info", message)
    logger.info(message)

def log_exception(presentation_service, logger, message, exception):
    "Registra y notifica la excepción completa de manera unificada"
    full_message = f"{message}: {exception}"
    presentation_service.notify("error", full_message)
    logger.exception(full_message)
