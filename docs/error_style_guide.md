# Guía de Estilo para Mensajes de Error

## Estructura Estándar

Todos los mensajes de error deben seguir este formato:

```
[TIPO]: Descripción concisa - Sugerencia de solución
```

## Tipos de Mensajes

- **ERROR**: Problema crítico que impide continuar una operación.
- **WARNING**: Situación potencialmente problemática pero no fatal.
- **INFO**: Información general del sistema.
- **DEBUG**: Información detallada para diagnóstico (solo visible en modo verbose).
- **CONFIRM**: Solicitud de confirmación al usuario.
- **INPUT**: Solicitud de entrada de datos al usuario.

## Recomendaciones

1. **Ser específico**: Mencionar exactamente qué falló (p.ej. "Error al conectar con API Telegram" en vez de "Error de conexión").

2. **Incluir contexto**: Añadir información relevante (p.ej. "Error al configurar webhook: URL inválida").

3. **Proponer solución**: Siempre que sea posible, incluir una sugerencia de acción correctiva.

4. **Consistencia**: Usar los mismos términos técnicos en toda la aplicación.

## Ejemplos

### Error crítico
```
[ERROR]: TELEGRAM_TOKEN no está definido en variables de entorno - Configure este valor en el archivo .env
```

### Advertencia
```
[WARNING]: Reintento 2/3 en 5 segundos - Verifique su conexión a internet
```

### Confirmación
```
[CONFIRM]: ¿Desea eliminar esta configuración? (s/n) - Esta acción no puede deshacerse
```
