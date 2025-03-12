"""
Path: src/cli/interface.py
Interfaz centralizada para interacción de línea de comandos.
"""

from src.console.console_interface import UnifiedConsoleInterface
from src.utils.config.app_config import (
    get_config,
)

class CLInterface:
    "Interfaz centralizada para interacción de línea de comandos."
    def __init__(self, verbose: bool = None, use_colors: bool = None):
        # Obtener valores de configuración global si no se especifican
        config = get_config()
        self.verbose = verbose if verbose is not None else config.verbose_mode
        use_colors_value = use_colors if use_colors is not None else config.use_colors
        self.console = UnifiedConsoleInterface(use_colors_value)
        # Se elimina la sincronización local a favor de centralizar en AppConfig

    def info(self, message: str, *args):
        " Muestra un mensaje informativo en la consola."
        self.console.info(message % args if args else message)

    def warning(self, message: str, *args):
        " Muestra un mensaje de advertencia en la consola."
        self.console.warning(message % args if args else message)

    def error(self, message: str, *args):
        " Muestra un mensaje de error en la consola."
        self.console.error(message % args if args else message)

    def debug(self, message: str, *args):
        " Muestra un mensaje de depuración en la consola."
        if self.verbose:
            self.console.debug(message % args if args else message)

    def confirm(self, message: str, default: bool = True) -> bool:
        " Pide confirmación al usuario para realizar una acción."
        result = self.console.confirm(message)
        return result if result is not None else default

    def input(self, message: str, default: str = None) -> str:
        " Solicita al usuario una entrada de texto."
        result = self.console.input(message)
        return result if result else (default or "")

    def section(self, title: str):
        " Muestra un título de sección en la consola."
        # Se usa la interfaz unificada para tener formato y colores consistentes
        self.console.info(f"[SECCIÓN] {title.upper()}")
        self.console.info("=" * (len(title) + 10))

# Singleton instance
cli = CLInterface()

def set_verbose(verbose: bool):
    "Establece el nivel de verbosidad de la interfaz."
    cli.verbose = verbose
    get_config().verbose_mode = verbose  # Configuración centralizada

def set_colors(use_colors: bool):
    "Establece el uso de colores en la interfaz"
    cli.console.use_colors = use_colors
    get_config().use_colors = use_colors  # Configuración centralizada

def info(message: str, *args, **kwargs):
    "Muestra un mensaje informativo en la consola."
    cli.info(message, *args, **kwargs)

def warning(message: str, *args, **kwargs):
    "Muestra un mensaje de advertencia en la consola."
    cli.warning(message, *args, **kwargs)

def error(message: str, *args, **kwargs):
    "Muestra un mensaje de error en la consola."
    cli.error(message, *args, **kwargs)

def debug(message: str, *args, **kwargs):
    "Muestra un mensaje de depuración en la consola."
    cli.debug(message, *args, **kwargs)

def confirm(message: str, default: bool = True) -> bool:
    "Pide confirmación al usuario para realizar una acción."
    return cli.confirm(message, default)

def get_input(message: str, default: str = None) -> str:
    "Solicita al usuario una entrada de texto."
    return cli.input(message, default)

def section(title: str):
    "Muestra un título de sección en la consola."
    cli.section(title)
