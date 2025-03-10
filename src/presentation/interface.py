"""
Path: src/presentation/interface.py
"""

import colorama
from src.console.console_interface import UnifiedConsoleInterface

class Interface:
    "Clase para mostrar mensajes en la consola con colores"
    def __init__(self, use_colors=True):
        colorama.init()
        self.use_colors = use_colors
        self.console = UnifiedConsoleInterface(use_colors)

    def info(self, message):
        " Muestra un mensaje informativo en la consola."
        self.console.info(message)

    def success(self, message):
        " Muestra un mensaje de éxito en la consola."
        self.console.success(message)

    def warn(self, message):
        " Muestra un mensaje de advertencia en la consola."
        self.console.warn(message)

    def error(self, message):
        " Muestra un mensaje de error en la consola."
        self.console.error(message)

    def debug(self, message):
        " Muestra un mensaje de depuración en la consola."
        self.console.debug(message)

    def confirm_action(self, question):
        " Pide confirmación al usuario para realizar una acción."
        return self.console.confirm(question)

    def prompt_input(self, message):
        " Solicita al usuario una entrada de texto."
        return self.console.input(message)
