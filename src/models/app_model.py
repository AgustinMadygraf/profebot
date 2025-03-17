"""
Path: src/models/app_model.py
"""

from typing import Optional, Dict, Any
from grpc import RpcError
from google.api_core.exceptions import GoogleAPIError
from pydantic import BaseModel
import google.generativeai as genai
from src.interfaces.llm_client import IStreamingLLMClient
from src.utils.logging.simple_logger import get_logger

_fallback_logger = get_logger()

# [ANÁLISIS] Clase TelegramUpdate:
# Esta clase se encarga de la validación y representación del update de Telegram.
# Nota: La lógica de comunicación externa (como el envío de mensajes mediante GeminiService)
# debería migrarse a la capa de servicios.
class TelegramUpdate(BaseModel):
    " Modelo para representar un objeto de actualización de Telegram "
    update_id: int
    message: Optional[Dict[str, Any]]
    def get_response(self) -> Optional[str]:
        """
        Procesa el mensaje recibido.
        Si es 'test' retorna el mensaje de prueba;
        de lo contrario, solo retorna el texto para que el controlador invoque al servicio Gemini.
        """
        if self.message:
            text = self.message.get('text')
            if text.lower() == 'test':
                return "¡Hola! ¿Cómo puedo ayudarte? <modo test>."
            # Se elimina la lógica de comunicación externa
            return text
        return None

    @staticmethod
    def parse_update(update: Dict[str, Any]) -> Optional["TelegramUpdate"]:
        " Parsea un objeto de actualización de Telegram "
        try:
            parsed = TelegramUpdate.parse_obj(update)
            return parsed
        except ValueError as e:
            _fallback_logger.error("Error parsing Telegram update: %s. Error: %s", update, e)
            return None

# [ANÁLISIS] Clase GeminiLLMClient:
# Esta clase encapsula la comunicación con el modelo Gemini.
# Nota: La función de envío de mensajes y streaming mezclan lógica de comunicación externa
# y manejo de sesiones.
# Se recomienda migrar esta parte a la capa de servicios para centralizar la integración con Gemini.
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
        Envía un mensaje al modelo y retorna la respuesta.
        Se recomienda: delegar la comunicación a un servicio especializado.
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
        Envía un mensaje al modelo con respuesta en modo streaming.
        Nota: La lógica de división en chunks podría centralizarse en la capa de servicios.
        """
        self._start_chat_session()
        if chunk_size <= 0:
            self.logger.warning("chunk_size (%d) no es válido. Se ajusta a 30.", chunk_size)
            chunk_size = 30
        try:
            response = self.chat_session.send_message(message)
            # Mejorar la división de la respuesta en chunks usando un generador
            full_response = ''.join(
                response.text[i:i + chunk_size] for i in range(0, len(response.text), chunk_size)
            )
            return full_response
        except Exception as e:
            self.logger.error("Error durante la respuesta streaming en Gemini: %s", e)
            raise

    def _start_chat_session(self):
        """
        Inicia la sesión de chat si no existe; si ya existe, intenta validar la sesión
        enviando un mensaje de prueba ("ping"). Si la sesión actual falla, se reinicia.
        """
        if self.chat_session:
            try:
                _ = self.chat_session.send_message("ping")
            except (RpcError, GoogleAPIError) as e:
                self.logger.warning("La sesión actual no responde, reiniciando sesión: %s", e)
                self.chat_session = None
        if not self.chat_session:
            try:
                self.chat_session = self.model.start_chat()
                self.logger.info("Sesión de chat iniciada con el modelo Gemini.")
            except (RpcError, GoogleAPIError) as e:
                self.logger.exception("Error iniciando sesión de chat en Gemini: %s", e)
                raise
