# Auditoría de Código - Separación de Responsabilidades

Este documento recopila los hallazgos en cuanto a la separación entre lógica de negocio y presentación.

## 1. Módulo: app_controller.py
- La función `process_update` mezcla la lógica de parseo y generación de respuesta (negocio) con llamadas directas a notificaciones (presentación) mediante `presentation_service.notify()` y métodos específicos como `show_update_processing`.
- La función `send_message` combina la verificación de datos del update (lógica de negocio) y la notificación basada en el resultado (presentación).

## 2. Módulo: webhook_configurator.py
- En el método `configure_webhook` se observa que se realizan notificaciones (a través de `self._notify` o directamente con `presentation_service.ask_for_retry`) junto con la lógica de reintentos y configuración del webhook.
- El método `_attempt_configure` captura excepciones y notifica errores en línea, combinando ambas responsabilidades.

## Conclusiones y Recomendaciones
- Se recomienda desacoplar la lógica de negocio de la presentación extrayendo la generación de mensajes y llamadas de notificación a métodos o módulos específicos.
- Considerar refactorizar funciones críticas para que solo gestionen la lógica de negocio y deleguen en una capa (por ejemplo, el PresentationService) la comunicación con el usuario.
- En pasos futuros (Subtarea 2.2), separar estas responsabilidades facilitará la mantenibilidad y pruebas del sistema.

*Este reporte servirá de base para planificar las refactorizaciones en pasos posteriores.*
