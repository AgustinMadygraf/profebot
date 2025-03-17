# Mapeo de Dependencias

## Dependencias Clave
- **LoggerService**: Se instancia en `src/utils/logging/simple_logger.py` y se utiliza en varios módulos.
- **TelegramMessagingService / IMessagingService**: Inyectado en `AppController` y utilizado para el envío de mensajes.
- **GeminiService**: Inyectado en `AppController` y usado para generar respuestas.
- **DatabaseConnectionManager**: Instanciado en `Application` para garantizar la existencia de la base de datos.
- **WebhookConfigService**: Inyectado en `Application` y ejecuta la configuración del webhook.

## Puntos de Creación
- `src/main.py`: Crea las dependencias en el método `create_dependencies()`.
- `src/controllers/app_controller.py`: Recibe las dependencias ya inyectadas.
- `src/services/telegram_service.py`: Realiza operaciones con la API de Telegram.

## Relaciones
- `AppController` depende de: IMessagingService, GeminiService, y LoggerService.
- `Application` actúa como contenedor y orquestador de estas dependencias.
