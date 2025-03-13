"""
Path: src/cli/interface.py
Interfaz centralizada para interacción de línea de comandos.
"""

from src.presentation.interface import Interface
from src.utils.config.app_config import get_config

cli = Interface()

def set_verbose(verbose: bool):
    """Establece el nivel de verbosidad de la interfaz."""
    cli.debug(f"Verbosidad actualizada a: {verbose}")
    get_config().verbose_mode = verbose

def set_colors(use_colors: bool):
    """Establece el uso de colores en la interfaz."""
    cli.info(f"Ajuste de colores a: {'habilitado' if use_colors else 'deshabilitado'}")
    get_config().use_colors = use_colors

def info(message: str, *args, **kwargs):
    """Muestra un mensaje informativo en la interfaz."""
    cli.info(message, *args, **kwargs)

def warning(message: str, *args, **kwargs):
    """Muestra un mensaje de advertencia en la interfaz."""
    cli.warning(message, *args, **kwargs)

def error(message: str, *args, **kwargs):
    """Muestra un mensaje de error en la interfaz."""
    cli.error(message, *args, **kwargs)

def debug(message: str, *args, **kwargs):
    """Muestra un mensaje de depuración en la interfaz."""
    cli.debug(message, *args, **kwargs)

def confirm(message: str) -> bool:
    """Solicita confirmación al usuario y retorna el resultado."""
    # Añadir sugerencia de formato si no está presente
    if "(s/n)" not in message:
        message = f"{message} (s/n)"
    # Se elimina el argumento 'default' ya que cli.confirm solo acepta un parámetro
    return cli.confirm(message)

def get_input(message: str, default: str = None) -> str:
    """Solicita una entrada de texto al usuario y retorna el valor ingresado."""
    return cli.input(message, default)

def section(title: str):
    """Muestra un título de sección en la interfaz."""
    cli.section(title)
