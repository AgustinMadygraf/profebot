"""
Path: src/models/app_model.py

"""

import os
import json
from typing import Optional, Dict, Any
from grpc import RpcError
from google.api_core.exceptions import GoogleAPIError
from pydantic import BaseModel
import google.generativeai as genai
from src.interfaces.llm_client import IStreamingLLMClient
from src.utils.logging.simple_logger import get_logger

_fallback_logger = get_logger()
class TelegramUpdate(BaseModel):
    " Modelo para representar un objeto de actualización de Telegram "
    update_id: int
    message: Optional[Dict[str, Any]]
    def get_response(self) -> Optional[str]:
        " Procesa el mensaje recibido y retorna una respuesta"
        if self.message:
            text = self.message.get('text')
            if text == 'test':
                return (
                    "¡Hola! ¿Cómo puedo ayudarte? <modo test>."
                )
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return "Error: GEMINI_API_KEY no configurado."
            try:
                system_instruction = self._load_system_instruction()
            except Exception as e:
                return str(e)
            client = GeminiLLMClient(api_key, system_instruction)
            try:
                return client.send_message(text)
            except (RpcError, GoogleAPIError) as e:
                return f"Error generando respuesta: {e}"
        return None

    def _load_system_instruction(self) -> str:
        "Carga las instrucciones del sistema desde el archivo de configuración."
        try:
            config_path = os.path.join(os.path.dirname(__file__), "../utils/config.json")
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            system_instruction = config.get("system_instructions", "Responde de forma amistosa.")
            if "system_instructions" in config:
                _fallback_logger.info("Instrucciones de sistema cargadas correctamente: %s", system_instruction)
            else:
                _fallback_logger.warning("No se encontró system_instructions en config, usando valor por defecto: %s", system_instruction)
            return system_instruction
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise Exception(f"Error leyendo config: {e}")

class GeminiLLMClient(IStreamingLLMClient):
    """
    Encapsula la lógica de interacción con el modelo de Gemini,
    implementando envío de mensajes y streaming.
    """
    def __init__(self, api_key: str, system_instruction: str, logger=None):
        """
        :param api_key: La clave de API para Gemini.
        :param system_instruction: Instrucciones del sistema (prompt inicial).
        :param logger: (Opcional) Logger inyectado. Usa _fallback_logger si no se provee.
        """
        self.api_key = api_key
        self.logger = logger if logger else _fallback_logger

        # Configurar la librería 'google.generativeai'
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
            system_instruction=system_instruction
        )

        self.chat_session = None
        self.logger.info("GeminiLLMClient inicializado correctamente.")

    def send_message(self, message: str) -> str:
        """
        Envía un mensaje al modelo y retorna la respuesta completa en texto.
        """
        self._start_chat_session()
        try:
            response = self.chat_session.send_message(message)
            return response.text
        except Exception as e:
            self.logger.error("Error al enviar mensaje a Gemini: %s", e)
            raise

    def send_message_streaming(self, message: str, chunk_size: int = 30) -> str:
        """
        Envía un mensaje al modelo y retorna la respuesta en modo streaming.
        Se va acumulando en un string final.
        """
        self._start_chat_session()
        try:
            response = self.chat_session.send_message(message)
            full_response = ""
            offset = 0
            while offset < len(response.text):
                chunk = response.text[offset:offset + chunk_size]
                full_response += chunk
                offset += chunk_size
            return full_response
        except Exception as e:
            self.logger.error("Error durante la respuesta streaming en Gemini: %s", e)
            raise

    def _start_chat_session(self):
        """
        Inicia la sesión de chat si no existe.
        """
        if not self.chat_session:
            self.chat_session = self.model.start_chat()
            self.logger.info("Sesión de chat iniciada con el modelo Gemini.")
