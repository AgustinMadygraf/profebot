# Interfaz IMessagingService

Esta interfaz define el contrato para el servicio de mensajería utilizado para interactuar con Telegram.

## Métodos Esperados

- **send_message(chat_id: int, text: str) -> Tuple[bool, Optional[str]]**  
  Envía un mensaje de texto al chat indicado y retorna un tuple que indica éxito y un mensaje de error en caso de fallo.
