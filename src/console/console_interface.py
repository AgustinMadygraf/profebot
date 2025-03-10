"""
Path: src/console/console_interface.py
"""

import colorama
from colorama import Fore, Style

class UnifiedConsoleInterface:
    "Clase para mostrar mensajes en la consola con colores"
    def __init__(self, use_colors=True):
        colorama.init()
        self.use_colors = use_colors

    def info(self, message):
        "Muestra un mensaje informativo en la consola."
        prefix = "[INFO]: "
        if self.use_colors:
            print(f"{Fore.CYAN}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def success(self, message):
        "Muestra un mensaje de éxito en la consola."
        prefix = "[SUCCESS]: "
        if self.use_colors:
            print(f"{Fore.GREEN}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def warning(self, message):
        "Muestra un mensaje de advertencia en la consola."
        prefix = "[WARNING]: "
        if self.use_colors:
            print(f"{Fore.YELLOW}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def error(self, message):
        "Muestra un mensaje de error en la consola."
        prefix = "[ERROR]: "
        if self.use_colors:
            print(f"{Fore.RED}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def debug(self, message):
        "Muestra un mensaje de depuración en la consola."
        prefix = "[DEBUG]: "
        if self.use_colors:
            print(f"{Fore.MAGENTA}{prefix}{message}{Style.RESET_ALL}")
        else:
            print(f"{prefix}{message}")

    def confirm(self, question):
        "Pide confirmación al usuario para realizar una acción."
        prefix = "[CONFIRM]: "
        if self.use_colors:
            response = input(f"{Fore.BLUE}{prefix}{question} (s/n): {Style.RESET_ALL}")
        else:
            response = input(f"{prefix}{question} (s/n): ")
        while response.lower() not in ['s', 'n']:
            print("Respuesta inválida. Por favor, ingrese 's' o 'n'.")
            response = input(f"{prefix}{question} (s/n): ")
        return response.lower().startswith('s')

    def input(self, message):
        "Pide al usuario que ingrese un valor."
        prefix = "[INPUT]: "
        if self.use_colors:
            return input(f"{Fore.BLUE}{prefix}{message}: {Style.RESET_ALL}")
        else:
            return input(f"{prefix}{message}: ")
