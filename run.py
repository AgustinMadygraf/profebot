"""
Path: run.py
"""

import os
import time
from fastapi import FastAPI
from dotenv import load_dotenv
from src.views.app_view import router as app_router
from src.controllers.app_controller import configure_webhook
from src.cli.interface import info, debug, error, warning, section
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
    info("Iniciando proceso de configuración del webhook...")

    for attempt in range(max_retries):
        if attempt > 0:
            warning("Reintento %d/%d de configuración del webhook...", attempt + 1, max_retries)
            time.sleep(retry_delay)
        else:
            info("Primer intento de configuración del webhook...")

        success, error_message = configure_webhook()
        if success:
            info("¡Webhook configurado correctamente!")
            return True

        if attempt < max_retries - 1:
            warning("Intento %d fallido: %s", attempt + 1, error_message)
        else:
            error("Último intento (%d/%d) fallido: %s",
                  max_retries, max_retries, error_message)

    return False

if __name__ == '__main__':
    section("Iniciando ProfeBot")
    debug("Cargando configuración...")

    # Configurar el webhook de Telegram con reintentos
    section("Configuración del webhook")
    if not try_configure_webhook():
        error("No se pudo configurar el webhook después de varios intentos.")
        error("El servidor iniciará, pero el bot podría no recibir mensajes.")
        error("Acciones recomendadas:")
        error("1. Verifique que TELEGRAM_TOKEN está configurado correctamente")
        error("2. Configure PUBLIC_URL en el archivo .env o")
        error("   Proporcione una URL pública válida cuando se solicite")
        error("3. Asegúrese de que la URL sea accesible")

    # Iniciar el servidor con uvicorn
    section("Iniciando servidor Web")
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    info("Servidor configurado en el puerto %d", port)
    info("Presione Ctrl+C para detener")
    uvicorn.run("run:app", host="0.0.0.0", port=port, reload=True)
