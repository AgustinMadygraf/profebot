"""
Path: src/views/app_view.py
"""

from flask import Blueprint, request, jsonify
from src.controllers.app_controller import process_update
from src.utils.logging.simple_logger import get_logger, log_exception
from src.configuration.central_config import CentralConfig

logger = get_logger()
blueprint = Blueprint('app', __name__)

@blueprint.route("/", methods=["GET"])
def index():
    "mensaje de bienvenida"
    return jsonify({"status": "ok", "message": "Bienvenido a la API de MadyGraf"})

@blueprint.route("/webhook", methods=["POST"])
def webhook():
    "Endpoint para recibir actualizaciones de Telegram, integrando el flujo unificado del webhook."
    update = request.get_json()
    logger.debug("webhook - Received update: %s", update)
    response = process_update(update)
    return jsonify({"status": "ok", "response": response})

@blueprint.errorhandler(Exception)
def handle_exception(e):
    "Manejador global de excepciones"
    log_exception(e)
    return jsonify({"status": "error", "detail": "Ocurrió un error interno"}), 500

@blueprint.route("/debug-config", methods=["GET"])
def debug_config():
    """"
    Endpoint de depuración para validar la centralización de configuraciones
    (solo para desarrollo)
    """
    if CentralConfig.ENVIRONMENT.lower() != "development":
        return jsonify({"error": "Acceso denegado"}), 403
    config_snapshot = {
         "DB_HOST": CentralConfig.DB_HOST,
         "DB_NAME": CentralConfig.DB_NAME,
         "PORT": CentralConfig.PORT,
         "ENVIRONMENT": CentralConfig.ENVIRONMENT
    }
    return jsonify(config_snapshot)
