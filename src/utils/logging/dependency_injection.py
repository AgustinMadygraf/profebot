"""
Path: utils/logging/dependency_injection.py
Simplified dependency injection for logging.
Provides access to loggers without complex configuration.
"""

import sys
from src.utils.logging.simple_logger import get_logger, set_verbose, is_verbose, initialize
from src.utils.config.app_config import get_config

# Initialize logging before anything else
initialize()

# Obtener configuración centralizada
config = get_config()

# Get command line arguments and update config
verbose_mode = "--verbose" in sys.argv
no_colors = "--no-colors" in sys.argv

# Actualizar configuración central utilizando el API de AppConfig
config.set("verbose_mode", verbose_mode)
config.set("use_colors", not no_colors)

# Get a logger for this module
_logger = get_logger("dependency_injection")

# Log inicial
if verbose_mode:
    _logger.debug("[VERBOSE] Modo verbose activado desde argumentos de línea de comandos")
else:
    _logger.info("[INFO] Modo estándar de logging (use --verbose para mensajes de debug)")

# Configuración de colores en CLI (se delega el valor desde AppConfig)
try:
    from src.cli.interface import set_verbose as cli_set_verbose
    cli_set_verbose(verbose_mode)
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

def get_injected_logger(name: str, config_override=None):
    """Retorna un logger configurado usando una instancia de configuración inyectada.
    Si se provee 'config_override', se usará esa instancia en vez de la configuración global.
    """
    config_instance = config_override if config_override is not None else get_config()
    # Se asume que 'get_logger' utiliza internamente la configuración
    return get_logger(name)

# Nueva función para inyección explícita de dependencias
def inject_dependencies(config_override=None) -> dict:
    """
    Devuelve un diccionario con las dependencias inyectadas, 
    facilitando testabilidad y configuraciones personalizadas.
    
    Retorna las siguientes dependencias:
      - "config": La instancia de configuración (usando config_override si se proporciona).
      - "logger": Un logger obtenido con get_injected_logger usando la instancia de configuración.
    
    Ejemplo de uso:
    
        deps = inject_dependencies()
        my_config = deps["config"]
        my_logger = deps["logger"]
    """
    config_instance = config_override if config_override is not None else get_config()
    # Se obtiene un logger por defecto ("default")
    injected_logger = get_injected_logger("default", config_override=config_instance)
    _logger.debug("Configuración inyectada: %s", config_instance)
    return {"config": config_instance, "logger": injected_logger}

# Export public functions
__all__ = ['get_logger', 'set_verbose', 'is_verbose', 'get_injected_logger', 'inject_dependencies']
