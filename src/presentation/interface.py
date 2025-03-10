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

    def warning(self, message):
        " Muestra un mensaje de advertencia en la consola, incluyendo recomendaciones."
        enhanced_message = message
        if "webhook" in message.lower():
            enhanced_message += " - Considere revisar la configuración del servidor o webhook."
        self.console.warning(enhanced_message)

    # Método de compatibilidad para código antiguo
    def warn(self, message):
        " Alias de warning para mantener retrocompatibilidad."
        return self.warning(message)

    def error(self, message):
        " Muestra un mensaje de error en la consola, agregando sugerencias si aplica."
        enhanced_message = message
        if "TELEGRAM_TOKEN" in message:
            enhanced_message += " - Verifique que TELEGRAM_TOKEN esté configurado correctamente."
        if "PUBLIC_URL" in message:
            enhanced_message += " - Asegúrese de proporcionar una URL pública válida."
        self.console.error(enhanced_message)

    def debug(self, message):
        " Muestra un mensaje de depuración en la consola."
        self.console.debug(message)

    def confirm_action(self, question):
        " Pide confirmación al usuario para realizar una acción."
        # Se agrega un mensaje aclaratorio antes de solicitar confirmación.
        question_with_hint = f"{question}\n(Responda 's' para confirmar o 'n' para cancelar)"
        return self.console.confirm(question_with_hint)

    def prompt_input(self, message):
        " Solicita al usuario una entrada de texto."
        return self.console.input(message)
