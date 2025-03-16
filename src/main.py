"""
Path: src/main.py
"""

import sys
import threading
from flask import Flask
from src.services.webhook_config_service import WebhookConfigService
from src.views.app_view import blueprint as app_blueprint
from src.configuration.central_config import CentralConfig
from src.utils.logging.simple_logger import get_logger, log_exception

logger = get_logger()
def create_app() -> Flask:
    """Crea y configura la aplicación Flask"""
    logger.debug("Argumentos de línea de comandos: %s", sys.argv)
    app = Flask(__name__)
    app.register_blueprint(app_blueprint)
    return app

def main():
    "Punto de entrada principal de la aplicación"
    app = create_app()
    port = CentralConfig.PORT
    logger.info("Servidor iniciándose en 0.0.0.0:%s", port)
    config_service = WebhookConfigService()
    threading.Thread(target=config_service.run_configuration, daemon=True).start()
    try:
        app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
    except (OSError, RuntimeError) as e:
        log_exception(e)
    finally:
        logger.info("El servidor se ha detenido")
