"""
Path: src/main.py

Actualización de documentación:
    La configuración del webhook ahora se centraliza en el servicio
    WebhookConfigService (ubicado en src/services/webhook_config_service.py).
    Este cambio permite una integración y mantenimiento más limpios del flujo
    de configuración, consolidando la obtención de URL pública, verificación y
    configuración del webhook en un único módulo.
"""

import sys
from flask import Flask
from src.configuration.webhook_conf import WebhookConfigurator
from src.views.app_view import blueprint as app_blueprint
from src.configuration.central_config import CentralConfig
from src.utils.logging.simple_logger import get_logger

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
    # Utiliza la configuración unificada del webhook a través de WebhookConfigService
    configurator = WebhookConfigurator()
    configurator.try_configure_webhook()
    try:
        app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
    except (OSError, RuntimeError) as e:
        logger.error("Error en la ejecución del servidor: %s", e)
        logger.debug("Caught exception: %s", e)
    finally:
        logger.info("El servidor se ha detenido")
