# ProfeBOT - Bot de Telegram para Asistencia Educativa

ProfeBOT es un bot de Telegram diseñado para proporcionar asistencia educativa. Utiliza FastAPI y Python, y está construido con una arquitectura modular y escalable.

---

## Requisitos

- Python 3.11 o superior
- FastAPI
- python-dotenv
- requests
- uvicorn
- google-generativeai (para GeminiLLM)

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/AgustinMadygraf/profebot
   ```
2. Instala las dependencias:
   ```bash
   cd profebot
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz del proyecto con al menos las siguientes variables:
   ```env
    TELEGRAM_TOKEN=your_telegram_bot_token_here
    GEMINI_API_KEY=your_gemini_api_key
   ```

---

## Configuración

### GeminiLLM

La configuración del prompt para GeminiLLM se carga desde un archivo de configuración JSON ubicado en `\utils\config.json`.  
Ejemplo de `config.json`:
```json
{
    "_path": "utils/config-example.json",
    "system_instructions": "Sos un bot de asistencia. Tu misión es brindar información y apoyo a los usuarios de esta comunidad. Responde de manera clara y útil.",
    "rules": [
        {
            "keywords": ["hola", "buenas", "saludos"],
            "response": "¡Hola! ¿En qué puedo ayudarte?"
        },
        {
            "keywords": ["quién eres", "qué eres", "quién sos"],
            "response": "Soy un asistente diseñado para brindarte información y asistencia."
        },
        {
            "keywords": ["qué puedes hacer", "cuáles son tus funciones"],
            "response": "Puedo responder preguntas, brindar ayuda y más."
        }
    ]
}
```

### Estructura del Proyecto

```
profebot/
├── src/
│   ├── controllers/
│   │   └── app_controller.py
│   ├── interfaces/
│   │   └── llm_client.py
│   ├── models/
│   │   └── app_model.py
│   └── views/
│       └── app_view.py
├── utils/
│   └── config.json
│   └── logging/
│       └── <archivos de configuración para logging>
├── .env
├── README.md
├── requirements.txt
└── run.py
```

---

## Uso

1. **Configuración del Webhook de Telegram:**  
   Ejecuta la aplicación. Al iniciarse, se intentará configurar el webhook de Telegram, solicitando la URL pública si es necesario.

2. **Iniciar el Servidor:**
   ```bash
   uvicorn run:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Documentación de la API:**  
   Accede a `http://localhost:8000/docs` para ver la documentación interactiva generada por FastAPI. La descripción de la API se genera a partir del contenido de este README.md.

---

## Contribución

Si deseas contribuir al proyecto, por favor sigue los siguientes pasos:

1. Realiza un fork del repositorio.
2. Crea una nueva rama:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y haz commit:
   ```bash
   git commit -m "Añade nueva funcionalidad"
   ```
4. Envía tu Pull Request.

---

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

---

## Contacto

Para cualquier consulta, puedes enviar un correo a [tu_correo@ejemplo.com](mailto:tu_correo@ejemplo.com).
