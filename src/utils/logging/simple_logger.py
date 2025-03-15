"""
Path: src/utils/logging/simple_logger.py
"""

import sys
import logging
import colorlog

# Configuración central del logger
logger = logging.getLogger("profebot")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Handler para salida en consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_logger() -> logging.Logger:
    """
    Obtiene un logger simple para la aplicación,
    configurando su nivel según los argumentos de la línea de comandos
    y utilizando colores en consola. Los campos 'filename' y 'levelname'
    se formatean para tener siempre 15 y 5 caracteres respectivamente, y el
    número de línea se reserva en 3 dígitos con relleno de ceros.
    """
    app_logger = logging.getLogger("app_logger")

    # Configurar el nivel del logger según si se pasó '--verbose' en la línea de comandos
    if '--verbose' in sys.argv:
        app_logger.setLevel(logging.DEBUG)
    else:
        app_logger.setLevel(logging.INFO)

    # Verifica si ya existen handlers para evitar duplicaciones
    if not app_logger.handlers:
        app_console_handler = logging.StreamHandler()
        app_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(filename)15.15s:%(lineno)03d - %(levelname)-5.5s - %(message)s",
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        app_console_handler.setFormatter(app_formatter)
        app_logger.addHandler(app_console_handler)

    return app_logger

def log_exception(e: Exception):
    """
    Función utilitaria para registrar excepciones de forma centralizada.
    """
    logger.exception("Exception occurred: %s", e)
