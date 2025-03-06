"""
Path: src/views/app_view.py
"""

from fastapi import APIRouter, Request
from src.controllers.app_controller import process_update

router = APIRouter()

@router.post("/")
async def telegram_webhook(request: Request):
    # Recibir el update de Telegram en formato JSON
    update = await request.json()
    # Procesar el update
    process_update(update)
    return {"status": "ok"}
