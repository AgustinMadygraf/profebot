"""
Path: utils/config/app_config.py
Configuración centralizada para la aplicación.
Proporciona un punto único para gestionar opciones globales.
"""

import sys
from typing import Dict, Any

class AppConfig:
    """
    Clase singleton que centraliza la configuración de la aplicación.
    
    NOTA:
      Esta clase unifica todas las configuraciones globales
      tales como 'verbose_mode' y 'use_colors'.
      Para obtener o actualizar un valor de configuración, utilice los métodos get() y set().
      
      Ejemplos de uso:
          config = get_config()
          verbose = config.get("verbose_mode", False)
          config.set("verbose_mode", True)
      
      Claves principales:
          - verbose_mode: bool   -> Activa el modo depuración.
          - use_colors: bool     -> Habilita/deshabilita colores en la salida.
          - max_retries: int     -> Número máximo de reintentos en procesos críticos.
          - retry_delay: int     -> Retardo (en segundos) entre reintentos.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la configuración con valores por defecto."""
        self._config: Dict[str, Any] = {
            "use_colors": True,
            "verbose_mode": False,
            "max_retries": 3,
            "retry_delay": 5
        }
        self._process_command_line_args()

    def __init__(self):
        # Se omite inicialización adicional para evitar duplicados.
        pass

    def _process_command_line_args(self):
        if not hasattr(self, '_config'):
            self._config: Dict[str, Any] = {
                "use_colors": True,
                "verbose_mode": False,
                "max_retries": 3,
                "retry_delay": 5
            }
        self._config["use_colors"] = "--no-colors" not in sys.argv

    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Establece un valor de configuración"""
        self._config[key] = value

    @property
    def verbose_mode(self) -> bool:
        """Indica si el modo verbose está activo"""
        return self._config.get("verbose_mode", False)

    @verbose_mode.setter
    def verbose_mode(self, value: bool) -> None:
        """Establece el modo verbose"""
        self._config["verbose_mode"] = value

    @property
    def use_colors(self) -> bool:
        """Indica si se deben usar colores"""
        return self._config.get("use_colors", True)

    @use_colors.setter
    def use_colors(self, value: bool) -> None:
        """Establece el uso de colores"""
        self._config["use_colors"] = value

# Crear instancia global
config = AppConfig()

# Funciones de conveniencia
def get_config() -> AppConfig:
    """Obtiene la instancia de configuración global"""
    return config

def is_verbose() -> bool:
    """Determina si el modo verbose está activo"""
    return config.verbose_mode

def should_use_colors() -> bool:
    """Determina si se deben usar colores"""
    return config.use_colors

def set_verbose(value: bool) -> None:
    """Establece el modo verbose"""
    config.verbose_mode = value

def set_colors(value: bool) -> None:
    """Establece el uso de colores"""
    config.use_colors = value
