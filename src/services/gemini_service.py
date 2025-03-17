"""
Path: src/services/gemini_service.py
"""

import google.generativeai as genai
from grpc import RpcError
from google.api_core.exceptions import GoogleAPIError

class GeminiService:
    " Servicio para interactuar con el modelo de lenguaje Gemini "
    def __init__(self, api_key: str, system_instruction: str, logger=None):
        self.logger = logger
        self.api_key = api_key
        self.system_instruction = system_instruction
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction=self.system_instruction
        )
        self.chat_session = None
        self.chat_history = []  # Nuevo buffer para almacenar el historial de chat
        self.logger.info("GeminiService inicializado correctamente.")

    def _is_critical_exception(self, e: Exception) -> bool:
        """
        Clasifica la excepción como crítica o no crítica.
        Retorna True si es crítica y requiere reiniciar la sesión.
        """
        # Ejemplo: tratar errores conocidos y clasificarlos según contenido.
        error_msg = str(e).lower()
        if "non-critical" in error_msg:
            return False
        return True

    def _start_chat_session(self):
        if self.chat_session:
            self.logger.debug("Verificando sesión actual con ping.")
            try:
                _ = self.chat_session.send_message("ping")
                self.logger.debug("Ping exitoso; la sesión se mantiene activa.")
            except (RpcError, GoogleAPIError) as e:
                self.logger.warning("Ping fallido. Detalle: %s", e)
                # Se evalúa si el error es crítico utilizando la nueva función:
                if self._is_critical_exception(e):
                    self.logger.warning("Error crítico detectado, reiniciando sesión.")
                    self.chat_session = None
                else:
                    self.logger.debug("Error no crítico; se mantiene la sesión.")
        if not self.chat_session:
            self.logger.debug("Iniciando nueva sesión de chat con Gemini.")
            try:
                self.chat_session = self.model.start_chat()
                self.logger.info("Sesión de chat iniciada con Gemini.")
            except (RpcError, GoogleAPIError) as e:
                self.logger.exception("Error iniciando sesión de chat en Gemini: %s", e)
                raise

    def send_message(self, message: str) -> str:
        " Send a message to the Gemini model and return the full response as text. "
        self._start_chat_session()
        self.logger.debug("Enviando mensaje: %s", message)
        try:
            response = self.chat_session.send_message(message)
            # Actualizar historial
            self.chat_history.append({"role": "user", "message": message})
            self.chat_history.append({"role": "gemini", "message": response.text})
            self.logger.debug("Historial actualizado: %s", self.chat_history)
            return response.text
        except Exception as e:
            self.logger.error("Error al enviar mensaje a Gemini: %s", e)
            raise

    def send_message_streaming(self, message: str, chunk_size: int = 30) -> str:
        """
        Send a message to the Gemini model and receive a streaming response.

        Args:
            message (str): The message to send.
            chunk_size (int): The size of each chunk in the streaming response.

        Returns:
            str: The streaming response from the Gemini model.
        """
        self._start_chat_session()
        if chunk_size <= 0:
            self.logger.warning("chunk_size (%d) no es válido. Se ajusta a 30.", chunk_size)
            chunk_size = 30
        self.logger.debug("Iniciando transmisión streaming para mensaje: %s", message)
        try:
            response = self.chat_session.send_message(message)
            self.logger.debug("Respuesta recibida con longitud: %d", len(response.text))
            full_text = ''.join(
                response.text[i:i + chunk_size] for i in range(0, len(response.text), chunk_size)
            )
            self.chat_history.append({"role": "user", "message": message})
            self.chat_history.append({"role": "gemini", "message": full_text})
            self.logger.debug("Historial actualizado (streaming): %s", self.chat_history)
            return full_text
        except Exception as e:
            self.logger.error("Error durante la respuesta streaming en Gemini: %s", e)
            raise
