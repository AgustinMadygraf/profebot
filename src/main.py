"""
Path: src/main.py
"""

import sys
import threading
from flask import Flask
from src.services.webhook_config_service import WebhookConfigService
from src.services.telegram_service import TelegramService
from src.configuration.central_config import CentralConfig
from src.utils.logging.simple_logger import get_logger, log_exception
from src.controllers.app_controller import AppController
from src.views.app_view import blueprint as app_blueprint

logger = get_logger()

def create_app(controller: AppController) -> Flask:
    """Crea y configura la aplicación Flask con inyección de dependencias"""
    logger.debug("Argumentos de línea de comandos: %s", sys.argv)
    app = Flask(__name__)

    app.config["controller"] = controller
    app.register_blueprint(app_blueprint)
    return app

def main():
    "Punto de entrada principal de la aplicación"

    telegram_service = TelegramService()

    controller_instance = AppController(telegram_service)

    app = create_app(controller_instance)
    port = CentralConfig.PORT
    logger.info("Servidor iniciándose en 0.0.0.0:%s", port)

    config_service = WebhookConfigService(telegram_service)
    threading.Thread(target=config_service.run_configuration, daemon=True).start()

    try:
        app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
    except (OSError, RuntimeError) as e:
        log_exception(e)
    finally:
        logger.info("El servidor se ha detenido")
