"""
Module: message_formatter.py

Provee una función centralizada para formatear mensajes siguiendo los estándares definidos,
permitiendo modificar el formato de salida sin afectar otras partes de la aplicación.
"""

def format_message(event: str, message: str) -> str:
    " Formatea un mensaje con un prefijo específico para un evento "
    prefixes = {
        "info": "[INFO] ",
        "success": "[SUCCESS] ",
        "warning": "[WARNING] ",
        "error": "[ERROR] ",
        "debug": "[DEBUG] "
    }
    prefix = prefixes.get(event.lower(), "")
    # Evitar prepender el prefijo si ya existe
    if not message.startswith(prefix):
        return prefix + message
    return message
