"""
Path: src/services/gemini_service.py
"""

import google.generativeai as genai
from grpc import RpcError
from google.api_core.exceptions import GoogleAPIError
from src.utils.logging.simple_logger import get_logger
from src.services.conversation_history_manager import ConversationHistoryManager

logger = get_logger()

class GeminiService:
    " Servicio para interactuar con el modelo de lenguaje Gemini "
    def __init__(self, api_key: str, system_instruction: str):
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
        self.history_manager = ConversationHistoryManager()
        logger.info("GeminiService inicializado correctamente.")

    def _start_chat_session(self):
        " Start a new chat session if the current one is not active. "
        if self.chat_session:
            try:
                _ = self.chat_session.send_message("ping")
                logger.debug("Chat session ping successful.")
            except (RpcError, GoogleAPIError) as e:
                logger.warning("Chat session ping failed, restarting session. Error: %s", e)
                self.chat_session = None
        if not self.chat_session:
            try:
                self.chat_session = self.model.start_chat()
                logger.info("Chat session started successfully.")
                logger.debug("New chat session initiated.")
            except (RpcError, GoogleAPIError) as e:
                logger.exception("Failed to start chat session: %s", e)
                raise

    def send_message(self, message: str) -> str:
        " Send a message to the Gemini model and return the full response as text. "
        self._start_chat_session()
        try:
            self.history_manager.add_message("user", message)
            logger.debug("Added user message to history: %s", message)
            logger.debug("Current history: %s", self.history_manager.get_history())
        except (RpcError, GoogleAPIError) as hist_e:
            logger.warning("Error adding user message to history: %s", hist_e)
        try:
            response = self.chat_session.send_message(message)
            logger.debug("Received response: %s", response.text)
            try:
                self.history_manager.add_message("assistant", response.text)
                logger.debug("Added assistant response to history: %s", response.text)
                logger.debug("Current history: %s", self.history_manager.get_history())
            except (RpcError, GoogleAPIError) as hist_e:
                logger.warning("Error adding assistant response to history: %s", hist_e)
            return response.text
        except Exception as e:
            logger.exception("Error sending message to Gemini: %s", e)
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
            logger.warning("chunk_size (%d) is invalid. Resetting to 30.", chunk_size)
            chunk_size = 30
        try:
            # Registrar mensaje del usuario en el historial
            self.history_manager.add_message("user", message)
            logger.debug("Added user streaming message to history: %s", message)
            logger.debug("Current history: %s", self.history_manager.get_history())
            response = self.chat_session.send_message(message)
            full_text = response.text
            logger.debug("Received streaming response: %s", full_text)
            # Registrar respuesta completa del asistente en el historial
            try:
                self.history_manager.add_message("assistant", full_text)
                logger.debug("Added streaming assistant response to history.")
                logger.debug("Current history: %s", self.history_manager.get_history())
            except (RpcError, GoogleAPIError) as hist_e:
                logger.warning("Error adding streaming response to history: %s", hist_e)
            return ''.join(
                full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)
            )
        except Exception as e:
            logger.exception("Error during streaming response from Gemini: %s", e)
            raise
