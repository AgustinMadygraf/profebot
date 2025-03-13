"""
Path: src/main.py
"""
import os
import sys
from flask import Flask
from dotenv import load_dotenv
from src.configuration.webhook_conf import WebhookConfigurator
from src.views.app_view import blueprint as app_blueprint
from src.utils.logging.simple_logger import get_logger

logger = get_logger()
def create_app() -> Flask:
    """Crea y configura la aplicación Flask"""
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()


    # Información de debugging
    logger.debug("Argumentos de línea de comandos: %s", sys.argv)

    app = Flask(__name__)

    # Registrar el blueprint con las rutas definidas en la vista
    app.register_blueprint(app_blueprint)

    return app


def main():
    "Punto de entrada principal de la aplicación"
    app = create_app()
    # Uso explícito de la configuración inyectada
    port = int(os.getenv("PORT", "8000"))
    logger.info("Servidor iniciándose en 0.0.0.0:%s", port)
    configurator = WebhookConfigurator()
    configurator.try_configure_webhook()
    try:
        app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
    except (OSError, RuntimeError) as e:
        logger.error("Error en la ejecución del servidor: %s", e)
        logger.debug("Caught exception: %s", e)
    finally:
        logger.info("El servidor se ha detenido")
