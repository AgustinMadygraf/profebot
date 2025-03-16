"""
Path: src/services/gemini_service.py
"""

import google.generativeai as genai
from grpc import RpcError
from google.api_core.exceptions import GoogleAPIError
from src.utils.logging.simple_logger import get_logger

class GeminiService:
    " Servicio para interactuar con el modelo de lenguaje Gemini "
    def __init__(self, api_key: str, system_instruction: str, logger=None):
        self.logger = logger if logger else get_logger()
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
        self.logger.info("GeminiService inicializado correctamente.")

    def _start_chat_session(self):
        if self.chat_session:
            try:
                _ = self.chat_session.send_message("ping")
            except (RpcError, GoogleAPIError) as e:
                self.logger.warning("La sesión actual no responde, reiniciando sesión: %s", e)
                self.chat_session = None
        if not self.chat_session:
            try:
                self.chat_session = self.model.start_chat()
                self.logger.info("Sesión de chat iniciada con Gemini.")
            except (RpcError, GoogleAPIError) as e:
                self.logger.exception("Error iniciando sesión de chat en Gemini: %s", e)
                raise

    def send_message(self, message: str) -> str:
        " Send a message to the Gemini model and return the full response as text. "
        self._start_chat_session()
        try:
            response = self.chat_session.send_message(message)
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
        try:
            response = self.chat_session.send_message(message)
            return ''.join(
                response.text[i:i + chunk_size] for i in range(0, len(response.text), chunk_size)
            )
        except Exception as e:
            self.logger.error("Error durante la respuesta streaming en Gemini: %s", e)
            raise
