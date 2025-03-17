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
from src.services.database_connection_manager import DatabaseConnectionManager
from src.services.config_repository import ConfigRepository
from src.services.gemini_service import GeminiService
from src.services.telegram_messaging_service import TelegramMessagingService

class Application:
    "Clase principal de la aplicación"
    def __init__(self, logger=None, controller=None, config_service=None):
        if not (logger and controller and config_service):
            logger, controller, config_service = self.create_dependencies()
        self.logger = logger
        self.controller = controller
        self.config_service = config_service
        self.app = self.create_app(self.controller)
        self.port = CentralConfig.PORT
        self.logger.info("Servidor iniciándose en 0.0.0.0:%s", self.port)

    def create_dependencies(self):
        " Crea las dependencias de la aplicación "
        logger = LoggerService()
        telegram_messaging_service = TelegramMessagingService()

        connection_manager = DatabaseConnectionManager(logger)
        connection_manager.create_database_if_not_exists()
        repo = ConfigRepository(connection_manager, logger)
        repo.initialize_configuration()
        system_instructions = repo.get_system_instructions()

        gemini_service = GeminiService(CentralConfig.GEMINI_API_KEY, system_instructions, logger)
        controller_instance = AppController(telegram_messaging_service, gemini_service, logger)
        config_service = WebhookConfigService(telegram_messaging_service, logger)
        return logger, controller_instance, config_service

    def create_app(self, controller: AppController) -> Flask:
        " Crea la aplicación Flask "
        app = Flask(__name__)
        app.config["controller"] = controller
        app.config["logger"] = self.logger
        app.register_blueprint(app_blueprint)
        return app

    def run(self):
        " Inicia la aplicación "
        threading.Thread(target=self.config_service.run_configuration, daemon=True).start()
        try:
            self.app.run(host="0.0.0.0", port=self.port, debug=True, use_reloader=False)
        except (OSError, RuntimeError) as e:
            log_exception(e)
        finally:
            self.logger.info("El servidor se ha detenido")
