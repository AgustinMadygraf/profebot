# Análisis del Archivo: src/models/app_model.py

## Resumen de Responsabilidades

1. Clase TelegramUpdate:
   - Validación y representación de actualizaciones de Telegram.
   - Lógica interna: Extrae y valida datos del update.
   - Comunicación externa: Realiza llamadas a GeminiService para obtener respuestas (debe migrarse a la capa de servicios).

2. Clase GeminiLLMClient:
   - Comunicación directa con el modelo Gemini (envío de mensajes y procesamiento en modo streaming).
   - Actualmente maneja la sesión y la división de la respuesta en chunks.
   - Se recomienda migrar esta lógica a un módulo de servicios especializado (por ejemplo, actualizar src/services/gemini_service.py).

## Recomendaciones para la Refactorización
- Separar las responsabilidades de validación y representación de la interacción con APIs externas.
- Mover la lógica de comunicación (LLM y envío de mensajes) a la capa de servicios.
- Mantener en los modelos únicamente la validación de datos y la representación interna, para mejorar la mantenibilidad y adherencia al patrón MVC.
