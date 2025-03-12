"""
Path: src/utils/event_dispatcher.py
"""

class EventDispatcher:
    "Clase para gestionar eventos y suscripciones"
    def __init__(self):
        self._listeners = {}

    def register(self, event_name, callback):
        "Registra un callback para un evento"
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def unregister(self, event_name, callback):
        "Elimina un callback de un evento"
        if event_name in self._listeners:
            self._listeners[event_name].remove(callback)

    def dispatch(self, event_name, *args, **kwargs):
        "Despacha un evento a los callbacks registrados"
        for callback in self._listeners.get(event_name, []):
            callback(*args, **kwargs)

# Instancia global (singleton)
dispatcher = EventDispatcher()
