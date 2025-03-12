"""
Path: src/presentation/interface.py
"""

import colorama
from src.console.console_interface import UnifiedConsoleInterface
from src.utils.config.app_config import get_config

class Interface:
    "Clase para mostrar mensajes en la consola con colores"
    def __init__(self, use_colors: bool = None):
        # Si no se especifica, se obtiene desde la configuración global
        if use_colors is None:
            use_colors = get_config().use_colors
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

    def prompt_retry(self, context):
        "Solicita al usuario confirmar si desea reintentar una acción."
        # Se reutiliza confirm_action para solicitar reintento
        return self.confirm_action(f"{context} - ¿Desea reintentar?")

    def confirm(self, message, default=True):
        "Alias para confirm_action, para tener la API unificada."
        return self.confirm_action(message)

    def input(self, message, default=""):
        "Alias para prompt_input, retornando un valor por defecto si la entrada es vacía."
        result = self.prompt_input(message)
        return result if result else default
        
    def section(self, title: str):
        """Muestra un título de sección en la interfaz."""
        self.console.info(f"[SECCIÓN] {title.upper()}")
        self.console.info("=" * (len(title) + 10))
