"""
Path: src/main.py
"""

import os
import sys
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from src.views.app_view import router as app_router
from src.controllers.app_controller import configure_webhook, get_public_url
from src.services.telegram_service import TelegramService
from src.presentation.presentation_service import PresentationService
from src.presentation.interface import Interface
from src.cli.interface import section
from src.utils.logging.dependency_injection import get_logger
from src.utils.config.app_config import is_verbose, should_use_colors

def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI"""
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener el logger simplificado
    logger = get_logger()

    # Información de debugging
    logger.debug("Argumentos de línea de comandos: %s", sys.argv)
    logger.debug("Modo verbose activo: %s", is_verbose())

    # Obtener la configuración centralizada

    app = FastAPI()

    # Incluir las rutas definidas en la vista
    app.include_router(app_router)

    return app

def try_configure_webhook(use_colors):
    """Intenta configurar el webhook de Telegram"""
    public_url, error = get_public_url()
    if not public_url:
        print(f"No se pudo obtener la URL pública: {error}")
        return False
    # Inicializar los servicios necesarios
    local_interface = Interface(use_colors=use_colors)  # Usar configuración centralizada
    local_presentation_service = PresentationService(local_interface)
    telegram_service = TelegramService()
    # Configurar el webhook
    success, error_message = configure_webhook(
        base_url=public_url,
        webhook_endpoint="webhook",  # Ajusta esto según tu configuración
        presentation_service=local_presentation_service,
        telegram_service=telegram_service
    )
    if success:
        print("Webhook configurado correctamente")
        return True
    else:
        print(f"Error al configurar webhook: {error_message}")
        return False

def main():
    "Punto de entrada principal de la aplicación"
    section("Iniciando ProfeBot")
    # Se agrega indicación de progreso según la guía de estilo de errores
    logger = get_logger()
    logger.info("[PROCESO] Configurando webhook, por favor espere...")
    _ = create_app()
    use_colors = should_use_colors()

    # Configurar el webhook de Telegram con reintentos
    try_configure_webhook(use_colors)

    # Iniciar el servidor con uvicorn
    port = int(os.getenv("PORT", "8000"))
    interface = Interface(use_colors=use_colors)  # Se pasa el parámetro use_colors
    presentation_service = PresentationService(interface)
    presentation_service.show_server_status(True, "0.0.0.0", port)
    uvicorn.run("src.main:create_app", host="0.0.0.0", port=port, reload=True)
