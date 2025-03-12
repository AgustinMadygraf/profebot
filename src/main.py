"""
Path: src/main.py
"""

import os
import sys
from flask import Flask
from dotenv import load_dotenv
from src.configuration.webhook_configurator import WebhookConfigurator
from src.views.app_view import blueprint as app_blueprint
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.cli.interface import section
from src.utils.logging.dependency_injection import get_logger
from src.utils.config.app_config import is_verbose, should_use_colors
from src.utils.error_handler import log_error, log_info

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


def main():
    "Punto de entrada principal de la aplicación"
    section("Iniciando ProfeBot")
    logger = get_logger()
    logger.info("[PROCESO] Configurando webhook, por favor espere...")
    app = create_app()
    use_colors = should_use_colors()
    port = int(os.getenv("PORT", "8000"))
    interface = Interface(use_colors=use_colors)
    presentation_service = PresentationService(interface)
    presentation_service.show_server_status(True, "0.0.0.0", port)
    configurator = WebhookConfigurator(use_colors)
    success = configurator.try_configure_webhook()
    logger.info("[PRUEBAS] Verificando integración de PresentationService...")
    if success:
        logger.info("[PRUEBAS] El webhook fue configurado correctamente.")
    else:
        logger.error("[PRUEBAS] Falló la configuración del webhook. Revise la salida y los logs.")
    try:
        app.run(host="0.0.0.0", port=port, debug=True)
    except (OSError, RuntimeError) as e:
        log_error(presentation_service, logger, "Error en la ejecución del servidor", e)
    finally:
        log_info(presentation_service, logger, "El servidor se ha detenido")
