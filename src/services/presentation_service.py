"""
Path: src/services/presentation_service.py
Servicio para manejar toda la lógica de presentación e interacción con el usuario.
Centraliza la comunicación con la interfaz CLI para mayor separación de responsabilidades.
"""

from src.cli.interface import (
    info, debug, error, warning, get_input, section
)

class PresentationService:
    """
    Servicio que encapsula toda la interacción con el usuario,
    separando completamente la lógica de presentación de la lógica de negocio.
    """

    @staticmethod
    def show_webhook_configuration_start():
        """Muestra mensaje de inicio de configuración del webhook."""
        section("Configuración del webhook")
        info("Por favor, proporcione la información necesaria para configurar "
             "el webhook de Telegram.")

    @staticmethod
    def show_webhook_configuration_success(url: str):
        """Muestra mensaje de éxito en la configuración del webhook."""
        info("¡Webhook configurado correctamente en: %s!", url)
        info("El bot ahora está listo para recibir mensajes.")

    @staticmethod
    def show_webhook_configuration_failure(error_message: str, attempt: int, max_attempts: int):
        """Muestra mensaje de fallo en la configuración del webhook."""
        if attempt < max_attempts:
            warning("Intento %d/%d fallido: %s", attempt, max_attempts, error_message)
        else:
            error("Último intento (%d/%d) fallido: %s", attempt, max_attempts, error_message)

    @staticmethod
    def show_webhook_retry_info(attempt: int, max_attempts: int, delay: int):
        """Muestra información sobre el reintento de configuración."""
        warning("Reintento %d/%d en %d segundos...", attempt + 1, max_attempts, delay)

    @staticmethod
    def show_webhook_all_attempts_failed():
        """Muestra mensaje cuando todos los intentos de configuración han fallado."""
        error("No se pudo configurar el webhook después de varios intentos.")
        error("El servidor iniciará, pero el bot podría no recibir mensajes.")
        error("Acciones recomendadas:")
        error("1. Verifique que TELEGRAM_TOKEN está configurado correctamente")
        error("2. Configure PUBLIC_URL en el archivo .env o")
        error("   Proporcione una URL pública válida cuando se solicite")
        error("3. Asegúrese de que la URL sea accesible")

    @staticmethod
    def ask_for_public_url():
        """
        Solicita al usuario la URL pública para el webhook.
        
        Returns:
            str: URL proporcionada por el usuario
        """
        info("Por favor, ingrese la URL pública temporal del servidor.")
        info("Ejemplo: https://abc123.ngrok.io")
        info("Nota: Asegúrese de incluir 'https://' al inicio")

        return get_input("URL pública: ").strip()

    @staticmethod
    def show_update_processing(update):
        """Muestra información sobre el procesamiento de un update de Telegram."""
        info("Procesando update de Telegram")
        debug("Datos del update: %s", update)

    @staticmethod
    def show_response_generated(response: str):
        """Muestra información sobre la respuesta generada."""
        info("Respuesta generada:")
        debug(response)

    @staticmethod
    def show_message_sent(chat_id: int):
        """Muestra confirmación de mensaje enviado."""
        info("Mensaje enviado correctamente al chat_id: %s", chat_id)

    @staticmethod
    def show_message_send_error(error_msg: str):
        """Muestra error al enviar mensaje."""
        error("Error al enviar mensaje: %s", error_msg)

    @staticmethod
    def show_server_start(port: int):
        """Muestra información sobre el inicio del servidor."""
        section("Iniciando servidor Web")
        info("Servidor configurado en el puerto %d", port)
        info("Presione Ctrl+C para detener")
