"""
Path: run.py
"""

from src.main import Application
from src.utils.logging.simple_logger import LoggerService

if __name__ == '__main__':
    logger = LoggerService()
    try:
        Application(logger=logger).run()
    except (RuntimeError, ValueError) as e:
        logger.exception("[run.py] Excepción no controlada: %s", e)
