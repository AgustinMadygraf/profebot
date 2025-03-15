"""
Path: src/configuration/app_config.py
"""

import warnings
from src.configuration.central_config import CentralConfig

warnings.warn(
    "AppConfig está deprecado. Utiliza CentralConfig en su lugar.",
    DeprecationWarning
)

# Se asigna CentralConfig a AppConfig para compatibilidad
AppConfig = CentralConfig
