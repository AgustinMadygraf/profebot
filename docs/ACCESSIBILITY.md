# Opciones de Accesibilidad en ProfeBot

Este documento describe las características de accesibilidad disponibles en ProfeBot, particularmente relacionadas con la salida en consola y el uso de colores.

## Desactivar Colores

Para usuarios con daltonismo o que utilizan consolas que no soportan colores ANSI, ProfeBot ofrece la opción de ejecutarse sin colores:

```bash
python run.py --no-colors
```

Esta opción hace que todos los mensajes de consola se muestren en texto plano sin formato de color.

## Modo Verbose

Para obtener información más detallada durante la ejecución, puede activar el modo verbose:

```bash
python run.py --verbose
```

Este modo muestra mensajes de nivel DEBUG que normalmente están ocultos, lo que puede ser útil para diagnosticar problemas.

## Combinar Opciones

Es posible combinar ambas opciones:

```bash
python run.py --no-colors --verbose
```

## Configuración Programática

Si está integrando ProfeBot en otra aplicación, puede configurar estas opciones programáticamente:

```python
from utils.logging.dependency_injection import set_verbose
from src.cli.interface import set_colors

# Desactivar colores
set_colors(False)

# Activar modo verbose
set_verbose(True)
```

## Soporte para Lectores de Pantalla

Los mensajes de consola están diseñados con prefijos claros para cada tipo de mensaje (INFO, WARNING, ERROR, DEBUG), lo que facilita su interpretación por lectores de pantalla.

## Problemas Conocidos

- Algunas terminales en Windows pueden no mostrar correctamente los colores ANSI.
- Los terminales que no soportan UTF-8 pueden mostrar caracteres extraños en ciertos mensajes.

Si encuentra problemas de accesibilidad, por favor reporte un issue en nuestro repositorio.
