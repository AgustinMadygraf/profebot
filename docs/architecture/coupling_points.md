# Puntos de Acoplamiento en la Arquitectura

Este documento identifica áreas donde la lógica de presentación y la lógica de negocio están estrechamente acopladas, lo que podría dificultar la extensibilidad futura.

## Principales Puntos de Acoplamiento

1. **Múltiples Servicios de Presentación**:
   - `src/services/presentation_service.py`
   - `src/presentation/presentation_service.py`
   
   Estos dos servicios implementan funcionalidades similares pero en diferentes contextos, causando duplicación y confusión.

2. **Interfaces Duplicadas**:
   - `src/presentation/interface.py`
   - `src/cli/interface.py`
   - `src/console/console_interface.py`
   
   Múltiples interfaces manejan la presentación en consola, con diferentes niveles de abstracción.

3. **Configuración de Colores y Verbose**:
   - `utils/logging/dependency_injection.py`
   - `run.py`
   
   La configuración se establece en diferentes puntos, lo que puede llevar a estados inconsistentes.

## Recomendaciones para Desacoplamiento

### Estructura Propuesta

1. **API Unificada de Presentación**:
   - Crear un único punto de entrada (`ConsolePresenter` o similar) que encapsule todas las interacciones de consola.
   - Todos los servicios deberían usar esta API en lugar de implementar su propia lógica de presentación.

2. **Centralización de Configuración**:
   - Implementar un patrón de configuración global o inyección de dependencias para manejar opciones como colores y verbose.
   - Todas las clases deberían recibir esta configuración en lugar de implementar su propia lógica.

3. **Separación Clara de Responsabilidades**:
   - Servicios de negocio: encapsulan lógica de dominio y operaciones
   - Servicios de presentación: encapsulan interacción con el usuario
   - Controladores: coordinan entre servicios
