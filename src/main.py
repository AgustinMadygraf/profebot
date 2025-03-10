"""
Path: src/main.py
"""

import os
import sys
from flask import Flask
from dotenv import load_dotenv
from src.views.app_view import blueprint as app_blueprint
from src.controllers.app_controller import get_public_url
from src.services.telegram_service import TelegramService
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.cli.interface import section
from src.utils.logging.dependency_injection import get_logger
from src.utils.config.app_config import is_verbose, should_use_colors

def create_app() -> Flask:
    """Crea y configura la aplicación Flask"""
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener el logger simplificado
    logger = get_logger()

    # Información de debugging
    logger.debug("Argumentos de línea de comandos: %s", sys.argv)
    logger.debug("Modo verbose activo: %s", is_verbose())

    app = Flask(__name__)

    # Registrar el blueprint con las rutas definidas en la vista
    app.register_blueprint(app_blueprint)

    return app

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
        presentation_service=local_presentation_service,
        telegram_service=telegram_service
    )
    if success:
        print("Webhook configurado correctamente")
        return True
    else:
        print(f"Error al configurar webhook: {error_message}")
        return False

def main():
    "Punto de entrada principal de la aplicación"
    section("Iniciando ProfeBot")
    # Indicación de progreso según la guía de estilo de errores
    logger = get_logger()
    logger.info("[PROCESO] Configurando webhook, por favor espere...")
    app = create_app()
    use_colors = should_use_colors()

    # Configurar el webhook de Telegram con reintentos
    try_configure_webhook(use_colors)

    # Iniciar el servidor Flask de desarrollo
    port = int(os.getenv("PORT", "8000"))
    interface = Interface(use_colors=use_colors)  # Se pasa el parámetro use_colors
    presentation_service = PresentationService(interface)
    presentation_service.show_server_status(True, "0.0.0.0", port)
    app.run(host="0.0.0.0", port=port, debug=True)

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
