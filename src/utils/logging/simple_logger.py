"""
Path: src/utils/logging/simple_logger.py
"""

import sys
import logging
import colorlog

def get_logger() -> logging.Logger:
    """
    Obtiene un logger simple para la aplicación,
    configurando su nivel según los argumentos de la línea de comandos
    y utilizando colores en consola. Los campos 'filename' y 'levelname'
    se formatean para tener siempre 15 y 5 caracteres respectivamente, y el
    número de línea se reserva en 3 dígitos con relleno de ceros.
    """
    logger = logging.getLogger("app_logger")

    # Configurar el nivel del logger según si se pasó '--verbose' en la línea de comandos
    if '--verbose' in sys.argv:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Verifica si ya existen handlers para evitar duplicaciones
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(filename)15.15s:%(lineno)03d - %(levelname)-5.5s - %(message)s",
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
