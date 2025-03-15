"""
Path: src/utils/validators.py
"""

def validate_telegram_update(update: dict) -> bool:
    " Valida un objeto update de Telegram, considerando campos alternativos como 'edited_message'. "
    if not isinstance(update, dict):
        return False
    # Permitir que el update contenga 'message' o 'edited_message'
    message = update.get("message") or update.get("edited_message")
    if not message or not isinstance(message, dict):
        return False
    chat = message.get("chat")
    if not chat or not isinstance(chat, dict) or "id" not in chat:
        return False
    return True
