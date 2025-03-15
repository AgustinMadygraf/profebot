"""
Path: src/views/app_view.py
"""

from flask import Blueprint, request, jsonify
from src.controllers.app_controller import process_update
from src.utils.logging.simple_logger import get_logger

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
    logger.exception("Unhandled exception: %s", e)
    return jsonify({"status": "error", "detail": "Ocurrió un error interno"}), 500
