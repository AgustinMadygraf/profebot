"""
Path: src/presentation/presentation_service.py
"""

from src.presentation.interface import Interface
from src.cli.interface import get_input, info

class PresentationService:
    " Servicio de presentación para mostrar mensajes al usuario "
    def __init__(self, interface: Interface):
        self.interface = interface

    def show_welcome_message(self):
        """Muestra el mensaje de bienvenida"""
        self.interface.info("=====================")
        self.interface.info("Bienvenido a MadyBot ")
        self.interface.info("=====================")

    def show_server_status(self, is_running, host=None, port=None):
        """Muestra el estado del servidor"""
        if is_running:
            self.interface.success(f"Servidor ejecutándose en http://{host}:{port}")
        else:
            self.interface.error("El servidor no está en ejecución")

    def show_webhook_status(self, is_set, details=None):
        """Muestra el estado del webhook"""
        if is_set:
            self.interface.success(f"Webhook configurado correctamente: {details}")
        else:
            self.interface.error("No se pudo configurar el webhook")

    def show_error_message(self, message):
        """Muestra un mensaje de error"""
        self.interface.error(message)

    def show_warning_message(self, message):
        """Muestra un mensaje de advertencia"""
        self.interface.warn(message)

    def show_debug_info(self, message):
        """Muestra información de depuración"""
        self.interface.debug(message)

    def show_process_status(self, stage, is_complete):
        """Muestra el estado de un proceso"""
        status = "Completado ✓" if is_complete else "En proceso..."
        self.interface.info(f"{stage}: {status}")

    def request_confirmation(self, action_description):
        """Solicita confirmación al usuario para una acción crítica
        
        Args:
            action_description (str): Descripción de la acción a confirmar
            
        Returns:
            bool: True si el usuario confirmó, False en caso contrario
        """
        return self.interface.confirm_action(action_description)

    def ask_for_retry(self, operation_name):
        """Pregunta al usuario si desea reintentar una operación
        
        Args:
            operation_name (str): Nombre de la operación que falló
            
        Returns:
            bool: True si el usuario desea reintentar, False en caso contrario
        """
        return self.interface.confirm_action(f"¿Desea reintentar {operation_name}?")

    def notify_operation_start(self, operation_name):
        """Notifica el inicio de una operación
        
        Args:
            operation_name (str): Nombre de la operación que se inicia
        """
        # Ahora el mensaje se transmite sin prefijo manual, se deja que la interfaz lo formatee
        self.interface.info(f"{operation_name}...")

    def notify_operation_progress(self, operation_name, step, total_steps):
        """Notifica el progreso de una operación
        
        Args:
            operation_name (str): Nombre de la operación
            step (int): Paso actual
            total_steps (int): Total de pasos
        """
        self.interface.info(f"{operation_name}: Paso {step} de {total_steps}")

    @staticmethod
    def ask_for_public_url():
        """
        Solicita al usuario la URL pública para el webhook.
        
        Returns:
            str: URL proporcionada por el usuario
        """
        message = (
            "Por favor, ingrese la URL pública temporal del servidor.\n"
            "Ejemplo: https://abc123.ngrok.io\n"
            "Nota: Asegúrese de incluir 'https://' al inicio"
        )
        info(message)  # Se muestra el mensaje consolidado
        return get_input("URL pública: ").strip()

    # Tarea 7: Ordenamiento y Centralización de mensajes de presentación
    @staticmethod
    def get_standard_templates():
        """
        Retorna un diccionario con plantillas estándar para mensajes.
        Facilita la centralización de textos comunes.
        """
        return {
            "welcome": "Bienvenido a MadyBot",
            "webhook_success": "Webhook configurado correctamente: {details}",
            "webhook_failure": "No se pudo configurar el webhook",
            "server_running": "Servidor ejecutándose en http://{host}:{port}",
            "server_stopped": "El servidor no está en ejecución",
        }

    # Tarea 8: Incremento de Flexibilidad para Futuras Ampliaciones
    # Permite registrar y llamar plugins para extender la funcionalidad de presentación.
    _plugins = {}

    @classmethod
    def register_plugin(cls, name: str, handler):
        """
        Registra un plugin de extensión para la presentación.

        Args:
            name (str): Nombre del plugin.
            handler: Función o método que maneje la extensión.
        """
        cls._plugins[name] = handler

    @classmethod
    def call_plugin(cls, name: str, *args, **kwargs):
        """
        Llama al plugin registrado identificado por 'name'.

        Args:
            name (str): Nombre del plugin.
        
        Returns:
            El resultado del plugin o None si no se encuentra.
        """
        if name in cls._plugins:
            return cls._plugins[name](*args, **kwargs)
        return None
