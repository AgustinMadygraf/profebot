"""
Path: src/utils/validators.py
"""

def validate_telegram_update(update: dict) -> bool:
    " Valida un objeto update de Telegram "
    if not isinstance(update, dict):
        return False
    message = update.get("message")
    if not message or not isinstance(message, dict):
        return False
    chat = message.get("chat")
    if not chat or not isinstance(chat, dict) or "id" not in chat:
        return False
    return True
