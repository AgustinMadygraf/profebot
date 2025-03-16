# Nuevo Diseño de Estructura de Carpetas

Se propone la siguiente reorganización para reflejar el patrón MVC y separar responsabilidades de forma clara:

- **/configuration**  
  Archivos de configuración y variables de entorno (ej. central_config.py).

- **/controllers**  
  Controladores que gestionan la lógica de la aplicación (ej. app_controller.py).

- **/models**  
  Modelos para validación y representación de datos (ej. app_model.py).

- **/services**  
  Lógica de comunicación externa e integración (ej. gemini_service.py, telegram_service.py, config_service.py).

- **/utils**  
  Utilidades compartidas (ej. logging, validaciones, etc.).

- **/views**  
  Vistas y endpoints de la aplicación (ej. app_view.py).

- **/docs**  
  Documentación técnica, análisis y diseño arquitectónico (incluye este archivo).

- **Raíz del proyecto**  
  Archivos de entrada como run.py y main.py.

Esta nueva organización facilita la escalabilidad, el mantenimiento y la adherencia a buenas prácticas de desarrollo.
