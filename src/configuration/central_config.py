"""
Path: src/configuration/central_config.py
Configuración central de la aplicación.
------------------------------------------------------------------------------
Actualización de la Configuración y Difusión:
- Se centralizan las variables críticas (por ejemplo, datos de BD, token de Telegram, clave API Gemini, puerto).
- Este módulo permite modificar la configuración clave sin tener que tocar múltiples archivos.
- Equipo: Revisen este módulo y ajusten las variables de entorno según su entorno (desarrollo, pruebas, producción).
- Ejemplo de uso:
      from src.configuration.central_config import CentralConfig
      print(CentralConfig.GEMINI_API_KEY)
------------------------------------------------------------------------------
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
