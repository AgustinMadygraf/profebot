"""
Path: src/services/conversation_history_manager.py
"""

class ConversationHistoryManager:
    """
    Módulo para gestionar el historial de conversación.
    Provee métodos para agregar mensajes y obtener el historial.
    """
    MAX_HISTORY_LENGTH = 10  # Umbral para resumir el historial

    def __init__(self):
        self.history = []

    def add_message(self, role: str, message: str):
        " Agrega un mensaje al historial con el rol especificado. "
        try:
            self.history.append({"role": role, "message": message})
            # Si el historial excede el umbral, se invoca al resumen
            if len(self.history) > self.MAX_HISTORY_LENGTH:
                self.history = self.summarize_history()
        except (TypeError, ValueError):
            # Se debe loguear o manejar el error según sea necesario
            pass

    def get_history(self):
        " Retorna el historial completo de la conversación. "
        return self.history

    def summarize_history(self):
        " Resumen del historial de conversación. "
        try:
            summarized = {
                "role": "system",
                "message": "[Historial resumido]: " + " | ".join(
                    msg["message"] for msg in self.history if msg["role"] in ("user", "assistant")
                )
            }
            return [summarized]
        except (TypeError, ValueError):
            # En caso de error, se retorna el historial original sin resumir.
            return self.history
