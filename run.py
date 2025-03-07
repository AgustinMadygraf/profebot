"""
Path: run.py
"""

import os
import time
from fastapi import FastAPI
from dotenv import load_dotenv
from src.views.app_view import router as app_router
from src.controllers.app_controller import configure_webhook
from utils.logging.dependency_injection import get_logger

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

    for attempt in range(max_retries):
        if attempt > 0:
            logger.info("Reintento %d/%d...", attempt + 1, max_retries)
            time.sleep(retry_delay)

        success, error_message = configure_webhook()
        if success:
            return True

        if attempt < max_retries - 1:
            logger.warning(f"Intento {attempt + 1} fallido: {error_message}")

    return False

if __name__ == '__main__':
    # Configurar el webhook de Telegram con reintentos
    logger.info("Iniciando configuración del webhook de Telegram...")
    if not try_configure_webhook():
        logger.warning("No se pudo configurar el webhook después de varios intentos.")
        logger.warning("El servidor iniciará, pero el bot podría no recibir mensajes.")
        logger.warning("Acciones recomendadas:")
        logger.warning("1. Verifique que TELEGRAM_TOKEN está configurado correctamente")
        logger.warning("2. Configure PUBLIC_URL en el archivo .env o")
        logger.warning("   Proporcione una URL pública válida cuando se solicite")
        logger.warning("3. Asegúrese de que la URL sea accesible")

    # Iniciar el servidor con uvicorn
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    logger.info("Iniciando servidor en el puerto %d", port)
    uvicorn.run("run:app", host="0.0.0.0", port=port, reload=True)
