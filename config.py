"""
Конфигурация для бота
"""
import os

# Токен можешь установить здесь ИЛИ через переменную окружения
# РЕКОМЕНДУЕТСЯ: использовать переменную окружения!
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Остальные настройки (если понадобятся)
DEBUG = os.getenv('DEBUG', 'False') == 'True'
LOG_FILE = 'bot.log'
