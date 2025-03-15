"""
Path: src/services/common_service_components.py
"""

def validate_service_token(token_name: str, token_value: str) -> tuple:
    """
    Valida que exista un token y emite un error genérico si no está definido.
    """
    if token_value:
        return True, None
    return False, f"{token_name} no definido"

def simulate_configure_webhook(webhook_url: str) -> tuple:
    """
    Función genérica que simula la configuración del webhook.  
    Se puede reemplazar con la lógica real de cada servicio.
    """
    if not webhook_url:
        return False, "URL de webhook vacía"
    # Aquí se realizarían llamadas al API real
    return True, None
