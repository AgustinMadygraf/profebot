"""
Path: src/configuration/central_config.py
Configuración central de la aplicación.
Administra las variables de entorno para la base de datos, la autenticación con Telegram, etc.
"""

import os
from dotenv import load_dotenv
from src.utils.logging.simple_logger import get_logger

logger = get_logger()

load_dotenv()

class CentralConfig:
    """
    Configuración central de la aplicación. 
    Define variables para la BD, tokens y claves de integración 
    incluyendo WhatsApp).
    """
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "mydb")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    # Variables para integración con WhatsApp
    WHATSAPP_API_KEY: str = os.getenv("WHATSAPP_API_KEY", "")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENV", "development")

    @classmethod
    def validate_configs(cls):
        """
        Valida que todas las variables de configuración críticas estén definidas,
        emitiendo advertencias en caso contrario.
        """
        missing = []
        if not cls.DB_HOST:
            missing.append("DB_HOST")
        if not cls.DB_USER:
            missing.append("DB_USER")
        if not cls.DB_PASSWORD:
            missing.append("DB_PASSWORD")
        if not cls.DB_NAME:
            missing.append("DB_NAME")
        if not cls.TELEGRAM_TOKEN:
            missing.append("TELEGRAM_TOKEN")
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        # Nuevas validaciones para WhatsApp
        if not cls.WHATSAPP_API_KEY:
            missing.append("WHATSAPP_API_KEY")
        if not cls.WHATSAPP_TOKEN:
            missing.append("WHATSAPP_TOKEN")
        if missing:
            logger.warning("Missing configuration variables: %s", ', '.join(missing))
        return missing
