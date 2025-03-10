# Guía de Uso de la API Unificada de Presentación

La API de presentación ofrece métodos estándar para interacción en consola:

- info(msg): mensajes informativos  
- warning(msg): advertencias  
- error(msg): errores graves  
- debug(msg): mensajes de depuración  
- confirm(msg): para solicitar confirmaciones (s/n)  
- input(msg): para tomar entradas de texto

Recomendaciones:
1. Utilizar estos métodos para mantener consistencia en la salida.  
2. Invocar confirm() antes de operaciones críticas.  
3. Consumir la lógica de colores y verbose desde los parámetros --no-colors y --verbose para prevenir inconsistencias.
