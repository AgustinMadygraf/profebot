"""
Path: run.py
"""

from src.main import main
from src.utils.logging.dependency_injection import get_injected_logger

if __name__ == '__main__':
    logger = get_injected_logger("run")
    logger.info("Iniciando la aplicación ProfeBot en run.py")
    main()
