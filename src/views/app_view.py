"""
Path: src/views/app_view.py
"""

from flask import Blueprint, request, jsonify
from src.controllers.app_controller import process_update
from src.utils.logging.dependency_injection import get_logger

blueprint = Blueprint('app', __name__)

@blueprint.route("/", methods=["POST"])
def telegram_webhook():
    """Procesa un update de Telegram y retorna una respuesta"""
    update = request.get_json()
    response_message = process_update(update)
    return jsonify({
        "status": "ok",
        "response": response_message if response_message else "No hay respuesta generada"
    })

@blueprint.route("/webhook", methods=["POST"])
def webhook():
    """Recibe el update de Telegram"""
    try:
        update = request.get_json()
        response = process_update(update)
        return jsonify({"status": "ok", "response": response})
    except (ValueError, KeyError, TypeError) as e:
        # Nuevo: registrar excepción con logger
        logger = get_logger("app_view")
        logger.exception("Exception processing webhook update: %s", e)
        return jsonify({"status": "error", "detail": str(e)}), 500
