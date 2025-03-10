# Guía de Uso de la API Unificada de Presentación

## Descripción General

La API de presentación ha sido unificada para proporcionar una interfaz consistente para interacciones en consola. Esta guía explica cómo usar la API correctamente siguiendo los estándares establecidos.

## Métodos Estándar

La API de presentación ofrece los siguientes métodos:

| Método | Propósito | Ejemplo |
|--------|-----------|---------|
| info(msg) | Mensajes informativos | `info("Proceso iniciado")` |
| warning(msg) | Advertencias | `warning("Archivo no encontrado - Se usará valor por defecto")` |
| error(msg) | Errores graves | `error("No se pudo conectar a la base de datos - Verifique credenciales")` |
| debug(msg) | Mensajes de depuración | `debug("Valor de variable x: 42")` |
| confirm(msg) | Solicitar confirmaciones | `confirm("¿Eliminar archivo? - Esta acción no puede deshacerse")` |
| get_input(msg) | Tomar entradas de texto | `get_input("Ingrese nombre de usuario")` |
| section(title) | Mostrar título de sección | `section("CONFIGURACIÓN")` |

## Configuración Global

La configuración de colores y verbosidad ahora está centralizada:

```python
from src.utils.config.app_config import get_config, set_verbose, set_colors

# Leer configuración
config = get_config()
is_verbose = config.verbose_mode
uses_colors = config.use_colors

# Modificar configuración
set_verbose(True)  # Activar modo verbose
set_colors(False)  # Desactivar colores
```

## Guía de Estilo de Mensajes

Para mantener consistencia, siga estas recomendaciones:

1. Utilizar los métodos estándar para cada tipo de mensaje
2. Seguir el formato: `[TIPO]: Mensaje - Sugerencia/Explicación`
3. Para confirmaciones, incluir las consecuencias de la acción
4. Para errores, siempre incluir una sugerencia de solución

## Documentación Relacionada

* [Guía de Estilo de Errores](error_style_guide.md)
* [Opciones de Accesibilidad](ACCESSIBILITY.md)
* [Puntos de Acoplamiento](architecture/coupling_points.md)
* [Estructura de Directorios](architecture/directory_structure.md)
* [Verificación de Compatibilidad](verification.md)
