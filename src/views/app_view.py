"""
Path: src/views/app_view.py
"""

from fastapi import APIRouter, Request
from src.controllers.app_controller import process_update

router = APIRouter()

@router.post("/")
async def telegram_webhook(request: Request):
    " Procesa un update de Telegram y retorna una respuesta "
    # Recibir el update de Telegram en formato JSON
    update = await request.json()
    # Procesar el update y obtener respuesta
    response_message = process_update(update)
    # Devolver la respuesta generada, o un status genérico
    return {
        "status": "ok",
        "response": response_message if response_message else "No hay respuesta generada"
    }
