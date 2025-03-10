"""
Path: src/presentation/interface.py
"""

import colorama
from colorama import Fore, Style

class Interface:
    "Clase para mostrar mensajes en la consola con colores"
    def __init__(self, use_colors=True):
        colorama.init()
        self.use_colors = use_colors

    def info(self, message):
        """Mostrar un mensaje de información"""
        prefix = "[INFO] "
        if self.use_colors:
            print(f"{Fore.CYAN}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def success(self, message):
        """Mostrar un mensaje de éxito"""
        prefix = "[SUCCESS] "
        if self.use_colors:
            print(f"{Fore.GREEN}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def warn(self, message):
        """Mostrar un mensaje de advertencia"""
        prefix = "[WARNING] "
        if self.use_colors:
            print(f"{Fore.YELLOW}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def error(self, message):
        """Mostrar un mensaje de error"""
        prefix = "[ERROR] "
        if self.use_colors:
            print(f"{Fore.RED}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def debug(self, message):
        """Mostrar un mensaje de depuración"""
        prefix = "[DEBUG] "
        if self.use_colors:
            print(f"{Fore.MAGENTA}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def confirm_action(self, question):
        """Solicita confirmación al usuario para una acción crítica
        
        Args:
            question (str): Pregunta a realizar al usuario
            
        Returns:
            bool: True si el usuario confirmó, False en caso contrario
        """
        prefix = "[CONFIRM] "
        if self.use_colors:
            response = input(f"{Fore.BLUE}{prefix}{question} (s/n): {Style.RESET_ALL}")
        else:
            response = input(f"{prefix}{question} (s/n): ")

        return response.lower().startswith('s')

    def prompt_input(self, message):
        """Solicita entrada de texto al usuario
        
        Args:
            message (str): Mensaje a mostrar al usuario
            
        Returns:
            str: Texto ingresado por el usuario
        """
        prefix = "[INPUT] "
        if self.use_colors:
            return input(f"{Fore.BLUE}{prefix}{message}: {Style.RESET_ALL}")
        else:
            return input(f"{prefix}{message}: ")
