"""
Path: src/llm_client.py

Definición de interfaces (ISP):
- IBaseLLMClient: interfaz base con el método esencial de envío de mensajes.
- IStreamingLLMClient: extiende de IBaseLLMClient e incluye envío en modo streaming.
"""

from abc import ABC, abstractmethod

class IBaseLLMClient(ABC):
    """
    Interfaz base para clientes LLM.
    Solo define la operación esencial de enviar un mensaje.
    
    Guía de uso:
    - Las implementaciones deben extender esta interfaz.
    - El método send_message debe enviar un mensaje y retornar la respuesta completa en texto.
    - Se deben manejar internamente las excepciones y loguear errores utilizando el logger.
    """
    @abstractmethod
    def send_message(self, message: str) -> str:
        """
        Envía un mensaje al modelo LLM y retorna la respuesta completa en texto.
        """
        raise NotImplementedError

class IStreamingLLMClient(IBaseLLMClient, ABC):
    """
    Interfaz para clientes LLM que también soportan el envío de mensajes en modo streaming.
    
    Guía de uso:
    - Las implementaciones deben extender esta interfaz.
    - El método send_message_streaming debe enviar el mensaje y
      retornar la respuesta en modo streaming,
      utilizando un mecanismo de chunking definido (por ejemplo, usando chunk_size).
    - Se recomienda manejar las excepciones y loguear errores utilizando el logger inyectado.
    """
    @abstractmethod
    def send_message_streaming(self, message: str, chunk_size: int = 30) -> str:
        """
        Envía un mensaje al modelo LLM y retorna la respuesta en modo streaming.
        """
        raise NotImplementedError
