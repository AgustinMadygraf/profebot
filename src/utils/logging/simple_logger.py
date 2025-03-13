"""
Path: src/utils/logging/simple_logger.py
"""

import sys
import logging

def get_logger() -> logging.Logger:
    """
    Obtiene un logger simple para la aplicación,
    configurando su nivel según los argumentos de la línea de comandos.
    """
    logger = logging.getLogger("app_logger")

    # Configurar el nivel del logger según si se pasó '--verbose' en la línea de comandos
    if '--verbose' in sys.argv:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Verifica si ya existen handlers para evitar duplicaciones
    if not logger.handlers:
        formatter = logging.Formatter("%(filename)s:%(lineno)d - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
