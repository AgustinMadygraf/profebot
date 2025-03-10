# Estructura de Directorios Propuesta

Esta es una propuesta de reorganización de directorios para mejorar la separación de responsabilidades y facilitar futuras extensiones.

```
profebot/
├── docs/                         # Documentación
│   ├── architecture/             # Documentación de arquitectura
│   ├── ui_guide.md               # Guía de uso de UI
│   ├── error_style_guide.md      # Guía de estilo para errores
│   └── ACCESSIBILITY.md          # Guía de accesibilidad
│
├── src/
│   ├── cli/                      # Interacción con línea de comandos
│   │   └── commands/             # Comandos específicos
│   │
│   ├── presentation/             # Capa de presentación unificada
│   │   ├── console/              # Presentación específica de consola
│   │   └── interfaces/           # Interfaces abstractas para diferentes UIs
│   │
│   ├── services/                 # Servicios de negocio
│   │   ├── telegram/             # Servicios específicos de Telegram
│   │   └── common/               # Servicios compartidos
│   │
│   ├── controllers/              # Controladores
│   ├── models/                   # Modelos de datos
│   └── views/                    # Vistas (para API)
│
└── utils/                        # Utilidades
    ├── config/                   # Configuración centralizada
    └── logging/                  # Utilidades de logging
```

## Principios de Organización

1. **Separación por Responsabilidad**:
   - `presentation`: Solo interacción con usuario
   - `services`: Solo lógica de negocio
   - `controllers`: Coordinación entre servicios

2. **Jerarquía Clara**:
   - Interfaces abstractas en nivel superior
   - Implementaciones concretas en subdirectorios

3. **Contextos Delimitados**:
   - Agrupar por funcionalidad relacionada
   - Minimizar dependencias entre contextos
