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
        self.interface.info("[INICIO] =====================")
        self.interface.info("[INICIO] Bienvenido a MadyBot ")
        self.interface.info("[INICIO] =====================")

    def show_server_status(self, is_running, host=None, port=None):
        """Muestra el estado del servidor"""
        if is_running:
            self.interface.success(f"[SERVIDOR] Ejecutándose en http://{host}:{port}")
        else:
            self.interface.error(
                "[SERVIDOR] El servidor no está en ejecución - Verifique los logs para más detalles"
            )

    def show_webhook_status(self, is_set, details=None):
        """Muestra el estado del webhook"""
        if is_set:
            self.interface.success(f"[WEBHOOK] Configurado correctamente: {details}")
        else:
            self.interface.error(
                "[WEBHOOK] No se pudo configurar el webhook - "
                "Verifique su conexión a internet y la URL proporcionada"
            )

    def show_error_message(self, message):
        """Muestra un mensaje de error siguiendo la guía de estilo"""
        # Agregar prefijo si no lo tiene
        if not message.startswith("[ERROR]"):
            message = f"[ERROR] {message}"
        self.interface.error(message)

    def show_warning_message(self, message):
        """Muestra un mensaje de advertencia siguiendo la guía de estilo"""
        # Agregar prefijo si no lo tiene
        if not message.startswith("[WARNING]"):
            message = f"[WARNING] {message}"
        # Cambiar método warn por warning para mantener consistencia
        self.interface.warning(message)

    def show_debug_info(self, message):
        """Muestra información de depuración siguiendo la guía de estilo"""
        # Agregar prefijo si no lo tiene
        if not message.startswith("[DEBUG]"):
            message = f"[DEBUG] {message}"
        self.interface.debug(message)

    def show_process_status(self, stage, is_complete):
        """Muestra el estado de un proceso"""
        status = "Completado ✓" if is_complete else "En proceso..."
        self.interface.info(f"{stage}: {status}")

    def request_confirmation(self, action_description):
        """Solicita confirmación al usuario para una acción crítica siguiendo la guía de estilo
        
        Args:
            action_description (str): Descripción de la acción a confirmar
            
        Returns:
            bool: True si el usuario confirmó, False en caso contrario
        """
        # Agregar información de las consecuencias si no la tiene
        if " - " not in action_description:
            action_description += " - Esta acción podría tener consecuencias importantes"
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

    def show_webhook_configuration_start(self):
        " Muestra el mensaje de inicio de configuración del webhook "
        self.interface.section("Configuración del webhook")
        self.interface.info(
            "Por favor, proporcione la información necesaria para configurar el webhook de Telegram"
        )

    def show_webhook_configuration_success(self, url: str):
        " Muestra el mensaje de éxito de configuración del webhook "
        self.interface.success(f"¡Webhook configurado correctamente en: {url}!")
        self.interface.info("El bot ahora está listo para recibir mensajes.")

    def show_webhook_configuration_failure(
        self, error_message: str, attempt: int, max_attempts: int
    ):
        " Muestra el mensaje de fallo de configuración del webhook "
        if attempt < max_attempts:
            self.interface.warning(
                f"[REINTENTO] Intento {attempt}/{max_attempts} fallido: "
                f"{error_message}"
            )
        else:
            self.interface.error(
                f"[FINAL] Último intento ({attempt}/{max_attempts}) fallido: "
                f"{error_message}"
            )

    def show_webhook_retry_info(self, attempt: int, max_attempts: int, delay: int):
        " Muestra información sobre un reintento de configuración del webhook "
        self.interface.warning(f"Reintento {attempt+1}/{max_attempts} en {delay} segundos...")

    def show_webhook_all_attempts_failed(self):
        " Muestra el mensaje de fallo de todos los intentos de configuración del webhook "
        full_message = (
            "[FALLO] No se pudo configurar el webhook después de varios intentos.\n"
            "[FALLO] El servidor iniciará, pero el bot podría no recibir mensajes.\n"
            "[SUGERENCIA] Acciones recomendadas:\n"
            "1. Verifique que TELEGRAM_TOKEN esté configurado correctamente\n"
            "2. Configure PUBLIC_URL en el archivo .env o proporcione una URL pública válida "
            "cuando se solicite\n"
            "3. Asegúrese de que la URL sea accesible"
        )
        self.interface.error(full_message)

    def show_update_processing(self, update):
        " Muestra un mensaje de depuración para el procesamiento de un update de Telegram "
        self.interface.info("Procesando update de Telegram")
        self.interface.debug(f"Datos del update: {update}")

    def show_response_generated(self, response: str):
        " Muestra un mensaje de depuración para la generación de una respuesta"
        self.interface.info("Respuesta generada:")
        self.interface.info(response)

    def show_message_sent(self, chat_id: int):
        " Muestra un mensaje de éxito al enviar un mensaje a un chat de Telegram "
        self.interface.info(f"Mensaje enviado correctamente al chat_id: {chat_id}")

    def show_message_send_error(self, error_msg: str):
        " Muestra un mensaje de error al enviar un mensaje a un chat de Telegram "
        self.interface.error(f"Error al enviar mensaje: {error_msg}")

    def show_server_start(self, port: int):
        " Muestra un mensaje de inicio del servidor web "
        self.interface.section("Iniciando servidor Web")
        self.interface.info(f"Servidor configurado en el puerto {port}")
        self.interface.info("Presione Ctrl+C para detener")
