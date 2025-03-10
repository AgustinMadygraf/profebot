"""
Path: run.py
"""

import os
import time
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from src.views.app_view import router as app_router
from src.controllers.app_controller import configure_webhook
from utils.logging.dependency_injection import get_logger
from src.services.presentation_service import PresentationService

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

logger = get_logger()

app = FastAPI()

# Incluir las rutas definidas en la vista
app.include_router(app_router)

def try_configure_webhook(max_retries=3, retry_delay=5):
    """
    Intenta configurar el webhook con reintentos
    """
    logger.info("Iniciando proceso de configuración del webhook...")
    PresentationService.show_webhook_configuration_start()

    for attempt in range(max_retries):
        if attempt > 0:
            logger.info("Reintento %d/%d", attempt + 1, max_retries)
            PresentationService.show_webhook_retry_info(attempt, max_retries, retry_delay)
            time.sleep(retry_delay)
        else:
            logger.info("Primer intento de configuración del webhook...")

        success, error_message = configure_webhook()
        if success:
            PresentationService.show_webhook_configuration_success("configuración actual")
            return True

        PresentationService.show_webhook_configuration_failure(
            error_message, attempt + 1, max_retries
        )

    PresentationService.show_webhook_all_attempts_failed()
    return False

def section(message):
    " Imprime un mensaje como una sección "
    logger.info(message)

if __name__ == '__main__':
    section("Iniciando ProfeBot")
    logger.debug("Cargando configuración...")

    # Configurar el webhook de Telegram con reintentos
    try_configure_webhook()

    # Iniciar el servidor con uvicorn
    port = int(os.getenv("PORT", "8000"))
    PresentationService.show_server_start(port)
    uvicorn.run("run:app", host="0.0.0.0", port=port, reload=True)
