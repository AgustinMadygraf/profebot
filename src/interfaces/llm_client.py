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
    """
    @abstractmethod
    def send_message(self, message: str) -> str:
        """
        Envía un mensaje al modelo LLM y retorna la respuesta completa en texto.
        """
        print("Enviando mensaje...")

    def another_method(self):
        "Another method"
        print("Another method")


class IStreamingLLMClient(IBaseLLMClient, ABC):
    """
    Interfaz para clientes LLM que también soportan envío de mensajes en modo streaming.
    """
    @abstractmethod
    def send_message_streaming(self, message: str, chunk_size: int = 30) -> str:
        """
        Envía un mensaje al modelo LLM y retorna la respuesta en modo streaming.
        """
        print("Enviando mensaje en modo streaming...")

    def another_method(self):
        "Another method"
        print("Another method")
