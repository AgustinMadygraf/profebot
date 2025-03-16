"""
Path: src/main.py
"""

import threading
from flask import Flask
from src.services.webhook_config_service import WebhookConfigService
from src.configuration.central_config import CentralConfig
from src.utils.logging.simple_logger import LoggerService, log_exception
from src.controllers.app_controller import AppController
from src.views.app_view import blueprint as app_blueprint
from src.services.config_service import get_system_instructions
from src.services.gemini_service import GeminiService
from src.services.telegram_messaging_service import TelegramMessagingService

def create_app(controller: AppController) -> Flask:
    """Crea y configura la aplicación Flask con inyección de dependencias."""
    app = Flask(__name__)
    app.config["controller"] = controller
    app.register_blueprint(app_blueprint)
    return app

def main():
    """
    Punto de entrada principal de la aplicación.
    Se centraliza la creación del LoggerService, inyectándolo en todos los componentes críticos 
    (TelegramMessagingService, GeminiService, AppController, WebhookConfigService) para asegurar
    un logging uniforme y facilitar la administración de dependencias.
    """
    # Crear instancia central del logger
    logger = LoggerService()

    telegram_messaging_service = TelegramMessagingService()
    gemini_service = GeminiService(CentralConfig.GEMINI_API_KEY, get_system_instructions(), logger)

    controller_instance = AppController(telegram_messaging_service, gemini_service, logger)

    app = create_app(controller_instance)
    port = CentralConfig.PORT
    logger.info("Servidor iniciándose en 0.0.0.0:%s", port)

    config_service = WebhookConfigService(telegram_messaging_service, logger)
    threading.Thread(target=config_service.run_configuration, daemon=True).start()

    try:
        app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
    except (OSError, RuntimeError) as e:
        log_exception(e)
    finally:
        logger.info("El servidor se ha detenido")
