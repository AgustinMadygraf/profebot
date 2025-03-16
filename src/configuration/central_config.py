"""
Path: src/configuration/central_config.py
Configuración central de la aplicación.
Administra las variables de entorno para la base de datos, la autenticación con Telegram, etc.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class CentralConfig:
    "Configuración central de la aplicación. Define variables para la BD, token de Telegram, etc."
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    # TELEGRAM_TOKEN: Token utilizado para autenticar con la API de Telegram.
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    PORT: int = int(os.getenv("PORT", "8000"))
