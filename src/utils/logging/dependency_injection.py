"""
Path: utils/logging/dependency_injection.py
Simplified dependency injection for logging.
Provides access to loggers without complex configuration.
"""

import sys
from src.utils.logging.simple_logger import get_logger, set_verbose, is_verbose, initialize
from src.utils.config.app_config import (
    get_config,
    set_verbose as config_set_verbose,
    set_colors as config_set_colors
)

# Initialize logging before anything else
initialize()

# Obtener configuración centralizada
config = get_config()

# Get command line arguments and update config
verbose_mode = "--verbose" in sys.argv
no_colors = "--no-colors" in sys.argv

# Configure verbose mode based on command line arguments
set_verbose(verbose_mode)
config_set_verbose(verbose_mode)  # Sincronizar con config global

# Get a logger for this module
_logger = get_logger("dependency_injection")

# Log initialization information
if verbose_mode:
    _logger.debug("[VERBOSE] Modo verbose activado desde argumentos de línea de comandos")
else:
    _logger.info("[INFO] Modo estándar de logging (use --verbose para mensajes de debug)")

# Import and configure CLI interface for colors
try:
    from src.cli.interface import set_colors, set_verbose as cli_set_verbose
    set_colors(not no_colors)
    cli_set_verbose(verbose_mode)
    config_set_colors(not no_colors)  # Sincronizar con config global

    if no_colors:
        _logger.info("[INFO] Salida de colores deshabilitada (--no-colors)")
except ImportError:
    _logger.debug("Interfaz CLI no disponible - configuración de colores no aplicada")

# For backward compatibility with any code that might use these
def get_debug_verbose():
    """For backward compatibility"""
    return is_verbose()

def set_debug_verbose(enabled=True):
    """For backward compatibility"""
    set_verbose(enabled)

def log_debug(message, *args, **kwargs):
    """For backward compatibility"""
    get_logger().debug(message, *args, **kwargs)

# Export public functions
__all__ = ['get_logger', 'set_verbose', 'is_verbose']
