"""
Path: src/views/app_view.py
"""

from flask import Blueprint, request, jsonify
from src.controllers.app_controller import process_update

blueprint = Blueprint('app', __name__)

@blueprint.route("/", methods=["POST"])
def telegram_webhook():
    """Procesa un update de Telegram y retorna una respuesta"""
    update = request.get_json()  # Obtener el JSON de la solicitud
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
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500
