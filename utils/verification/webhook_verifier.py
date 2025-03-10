"""
Path: utils/verification/webhook_verifier.py
Herramienta para verificar el funcionamiento correcto del webhook de Telegram.
"""

import os
from typing import Tuple, Optional
import requests

class WebhookVerifier:
    """
    Clase de utilidad para verificar el estado y funcionamiento del webhook de Telegram.
    """

    @staticmethod
    def get_webhook_info() -> Tuple[bool, dict, Optional[str]]:
        """
        Verifica el estado actual del webhook configurado en Telegram.
        
        Returns:
            Tuple[bool, dict, Optional[str]]: (éxito, datos_webhook, mensaje_error)
        """
        token = os.getenv("TELEGRAM_TOKEN")
        if not token:
            return False, {}, "TELEGRAM_TOKEN no está definido en las variables de entorno"

        try:
            url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('ok'):
                return True, data.get('result', {}), None
            else:
                return False, {}, (
                    f"Error de API Telegram: {data.get('description', 'Sin detalles')}"
                )

        except requests.exceptions.RequestException as e:
            return False, {}, f"Error de conexión: {str(e)}"

    @staticmethod
    def send_test_message(
        chat_id: int, message: str = "Mensaje de prueba"
    ) -> Tuple[bool, Optional[str]]:
        """
        Envía un mensaje de prueba para verificar la conectividad.
        
        Args:
            chat_id: ID del chat donde enviar el mensaje
            message: Mensaje a enviar
        
        Returns:
            Tuple[bool, Optional[str]]: (éxito, mensaje_error)
        """
        token = os.getenv("TELEGRAM_TOKEN")
        if not token:
            return False, "TELEGRAM_TOKEN no está definido en las variables de entorno"

        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('ok'):
                return True, None
            else:
                return False, f"Error de API Telegram: {data.get('description', 'Sin detalles')}"

        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"

# Función de utilidad para verificación rápida
def verify_webhook_setup():
    """
    Verifica la configuración actual del webhook y muestra un informe.
    
    Returns:
        bool: True si todo está correctamente configurado, False en caso contrario
    """
    success, info, error = WebhookVerifier.get_webhook_info()

    if not success:
        print(f"[ERROR] No se pudo obtener información del webhook: {error}")
        return False

    if not info.get('url'):
        print("[ERROR] No hay URL de webhook configurada")
        return False

    print(f"[INFO] Webhook configurado en: {info.get('url')}")
    estado_webhook = (
        'Activo' if info.get('has_custom_certificate', False) 
        else 'Sin certificado personalizado'
    )
    print(f"[INFO] Estado del webhook: {estado_webhook}")
    print(f"[INFO] Mensajes pendientes: {info.get('pending_update_count', 0)}")

    if info.get('last_error_date'):
        print(f"[WARNING] Último error: {info.get('last_error_message', 'Sin detalles')}")

    return 'url' in info and info['url']
