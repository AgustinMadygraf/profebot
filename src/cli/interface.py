"""
Path: src/cli/interface.py
Interfaz centralizada para interacción de línea de comandos.
"""

from src.console.console_interface import UnifiedConsoleInterface

class CLInterface:
    "Interfaz centralizada para interacción de línea de comandos."
    def __init__(self, verbose: bool = False, use_colors: bool = True):
        self.verbose = verbose
        self.console = UnifiedConsoleInterface(use_colors)

    def info(self, message: str, *args):
        " Muestra un mensaje informativo en la consola."
        self.console.info(message % args if args else message)

    def warning(self, message: str, *args):
        " Muestra un mensaje de advertencia en la consola."
        self.console.warn(message % args if args else message)

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

def set_colors(use_colors: bool):
    "Establece el uso de colores en la interf"
    cli.console.use_colors = use_colors

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
