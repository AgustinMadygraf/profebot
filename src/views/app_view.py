"""
Path: src/views/app_view.py
"""

from flask import Blueprint, request, jsonify, current_app
from src.utils.logging.simple_logger import get_logger, log_exception

logger = get_logger()
blueprint = Blueprint('app', __name__)

@blueprint.route("/", methods=["GET"])
def index():
    "Mensaje de bienvenida"
    return jsonify({"status": "ok", "message": "Bienvenido a la API de MadyGraf"})

@blueprint.route("/webhook", methods=["POST"])
def webhook():
    "Endpoint para recibir actualizaciones de Telegram, integrando el flujo unificado del webhook."
    update = request.get_json()
    logger.debug("webhook - Received update: %s", update)

    controller = current_app.config.get("controller")
    if not controller:
        logger.error("Controlador no encontrado en la configuración de la aplicación")
        return jsonify({"status": "error", "detail": "Controlador no configurado"}), 500

    response = controller.process_update(update)
    return jsonify({"status": "ok", "response": response})

@blueprint.errorhandler(Exception)
def handle_exception(e):
    "Manejador global de excepciones"
    log_exception(e)
    return jsonify({"status": "error", "detail": "Ocurrió un error interno"}), 500
