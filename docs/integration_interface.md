# Interfaz de Integración para Servicios de Mensajería

Esta documentación describe la interfaz y responsabilidades que debe cumplir cualquier servicio de mensajería implementado en el sistema.

## Interfaz Base: MessagingServiceBase
La interfaz definida en `src/services/messaging_base_service.py` especifica los siguientes métodos obligatorios que deben implementarse:

- **validate_token()**  
  Valida que el token de autenticación esté definido y tenga el formato correcto.

- **configure_webhook(url: str)**  
  Configura el webhook en la API de mensajería, utilizando la URL pública proporcionada.

- **get_webhook_info()**  
  Obtiene información del estado del webhook configurado.

- **send_message(chat_id: int, text: str)**  
  Envía un mensaje al chat especificado.

## Notas de Implementación

- **Consistencia:**  
  Cualquier servicio (por ejemplo, Telegram o futuros servicios como WhatsApp) deberá implementar esta interfaz para garantizar consistencia en la configuración y el envío de mensajes.

- **Separación de Responsabilidades:**  
  La implementación debe separar la lógica de negocio de la integración con la API (por ejemplo, la construcción de URLs y el manejo de solicitudes HTTP) para facilitar la reutilización y el mantenimiento.

- **Extensibilidad:**  
  Se recomienda que nuevos servicios de mensajería derivan de `MessagingServiceBase` y compartan la lógica común cuando sea posible, centralizando validaciones y manejo de errores.

## Ejemplo de Implementación

El servicio de Telegram, definido en `src/services/telegram_service.py`, es un ejemplo de cómo implementar la interfaz:

```python
class TelegramService(MessagingServiceBase):
    def validate_token(self) -> Tuple[bool, Optional[str]]:
        # Delegar en una función de validación (p.ej., validate_telegram_token)
        ...

    def configure_webhook(self, url: str) -> Tuple[bool, Optional[str]]:
        # Construir la URL y realizar la solicitud HTTP correspondiente
        ...

    def get_webhook_info(self) -> Tuple[bool, Any]:
        # Realizar la petición para obtener información del webhook
        ...

    def send_message(self, chat_id: int, text: str) -> Tuple[bool, Optional[str]]:
        # Enviar el mensaje a través de la API de Telegram
        ...
```

Esta documentación servirá como guía para futuros desarrolladores que implementen nuevos canales de mensajería o necesiten modificar la integración existente.

> **Nota:** Asegúrese de mantener la documentación sincronizada con los cambios en la implementación.
