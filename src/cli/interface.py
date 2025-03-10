"""
Path: src/cli/interface.py
Interfaz centralizada para interacción de línea de comandos.
"""

import logging
import sys
from typing import Optional, Any

# Definiciones de colores ANSI para la consola
class Colors:
    """Colores ANSI para formatos de consola."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Colores de texto
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Colores de fondo
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @classmethod
    def disabled(cls):
        """Deshabilita todos los colores estableciéndolos a cadenas vacías."""
        for attr_name in dir(cls):
            if not attr_name.startswith("__") and isinstance(getattr(cls, attr_name), str):
                setattr(cls, attr_name, "")

class CLInterface:
    """Centralized CLI interaction module for ProfeBot."""

    def __init__(self, verbose: bool = False, use_colors: bool = True):
        self.verbose = verbose
        self.use_colors = use_colors
        self.logger = logging.getLogger('profebot.cli')
        
        # Deshabilitamos colores si no se solicitan
        if not use_colors:
            Colors.disabled()

    def format_message(self, level: str, message: str, *args, **kwargs) -> str:
        """
        Formatea un mensaje para mostrar en la consola según su nivel.
        
        Args:
            level: Nivel del mensaje (INFO, WARNING, ERROR, DEBUG)
            message: Mensaje a formatear
            *args: Argumentos para el formato del mensaje
            
        Returns:
            Mensaje formateado con colores y prefijos
        """
        # Si hay argumentos, aplicar formato
        if args:
            try:
                message = message % args
            except (TypeError, ValueError) as e:
                # Si hay un error de formato, mostrar mensaje original
                message = f"{message} (Error de formato: {e})"
        
        # Aplicar formato según el nivel
        if level == "INFO":
            prefix = f"{Colors.GREEN}{Colors.BOLD}INFO:{Colors.RESET} "
        elif level == "WARNING":
            prefix = f"{Colors.YELLOW}{Colors.BOLD}AVISO:{Colors.RESET} "
        elif level == "ERROR":
            prefix = f"{Colors.RED}{Colors.BOLD}ERROR:{Colors.RESET} "
        elif level == "DEBUG":
            prefix = f"{Colors.BLUE}{Colors.BOLD}DEBUG:{Colors.RESET} "
        else:
            prefix = f"{level}: "
            
        return f"{prefix}{message}"

    def info(self, message: str, *args, **kwargs):
        """Display informational message."""
        self.logger.info(message, *args, **kwargs)
        formatted_message = self.format_message("INFO", message, *args)
        print(formatted_message)

    def warning(self, message: str, *args, **kwargs):
        """Display warning message."""
        self.logger.warning(message, *args, **kwargs)
        formatted_message = self.format_message("WARNING", message, *args)
        print(formatted_message)

    def error(self, message: str, *args, **kwargs):
        """Display error message."""
        self.logger.error(message, *args, **kwargs)
        formatted_message = self.format_message("ERROR", message, *args)
        print(formatted_message)

    def debug(self, message: str, *args, **kwargs):
        """Display debug message (only if verbose)."""
        self.logger.debug(message, *args, **kwargs)
        if self.verbose:
            formatted_message = self.format_message("DEBUG", message, *args)
            print(formatted_message)

    def confirm(self, message: str, default: bool = True) -> bool:
        """Ask for user confirmation."""
        prompt = f"{Colors.CYAN}{message}{Colors.RESET}"
        options = f" [{Colors.GREEN}Y{Colors.RESET}/{Colors.RED}n{Colors.RESET}]: " if default else f" [{Colors.GREEN}y{Colors.RESET}/{Colors.RED}N{Colors.RESET}]: "
        response = input(prompt + options)
        if not response:
            return default
        return response.lower() in ['y', 'yes', 'si', 's']

    def input(self, message: str, default: Optional[str] = None) -> str:
        """Get user input with optional default value."""
        prompt = f"{Colors.CYAN}{message}{Colors.RESET}"
        if default:
            prompt += f" [{Colors.YELLOW}{default}{Colors.RESET}]: "
        else:
            prompt += f": "
        response = input(prompt)
        return response if response else default or ""

    def section(self, title: str):
        """Display a section header."""
        border = "=" * (len(title) + 6)
        print(f"\n{Colors.CYAN}{Colors.BOLD}{border}")
        print(f"   {title.upper()}   ")
        print(f"{border}{Colors.RESET}\n")

# Singleton instance
cli = CLInterface()

# Convenience functions
def set_verbose(verbose: bool):
    """Set verbosity level for CLI messages."""
    cli.verbose = verbose

def set_colors(use_colors: bool):
    """Enable or disable colors in CLI messages."""
    cli.use_colors = use_colors
    if not use_colors:
        Colors.disabled()

def info(message: str, *args, **kwargs):
    """Display informational message."""
    cli.info(message, *args, **kwargs)

def warning(message: str, *args, **kwargs):
    """Display warning message."""
    cli.warning(message, *args, **kwargs)

def error(message: str, *args, **kwargs):
    """Display error message."""
    cli.error(message, *args, **kwargs)

def debug(message: str, *args, **kwargs):
    """Display debug message (only shown if verbose mode is enabled)."""
    cli.debug(message, *args, **kwargs)

def confirm(message: str, default: bool = True) -> bool:
    """Ask for user confirmation with yes/no options."""
    return cli.confirm(message, default)

def get_input(message: str, default: Optional[str] = None) -> str:
    """Get text input from user with optional default value."""
    return cli.input(message, default)

def section(title: str):
    """Display a formatted section header to organize output."""
    cli.section(title)
