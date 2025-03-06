# ProfeBOT - Bot de Telegram para Asistencia Educativa

## Descripción
ProfeBOT es un bot de Telegram diseñado para proporcionar asistencia educativa. Está construido con FastAPI y Python, implementando una arquitectura modular y escalable.

## Requisitos
- Python 3.11 o superior
- FastAPI
- python-dotenv
- requests
- uvicorn

## Configuración

### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto con:

```env
TELEGRAM_TOKEN=tu_token_de_telegram
PUBLIC_URL=url_publica_del_servidor  # Opcional
PORT=8000  # Puerto para el servidor (opcional, default: 8000)
```

### Estructura del Proyecto
