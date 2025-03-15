"""
Path: run.py
"""

from src.configuration.central_config import CentralConfig
from src.main import main
from src.utils.logging.simple_logger import get_logger

logger = get_logger()
print("\033[H\033[J")
logger.info("Ambiente actual: %s", CentralConfig.ENVIRONMENT)
if __name__ == '__main__':
    main()
