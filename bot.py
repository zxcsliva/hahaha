import logging
import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
from solutions import ALL_SOLUTIONS

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("Бот запускается...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_text = (
        "🤖 ЙО, ДОБРО ПОЖАЛОВАТЬ В ТЕХПОДДЕРЖКУ! 🤖\n\n"
        "Я - ЛЕГЕНДАРНЫЙ БОТ ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ!\n"
        "Просто напиши мне о своей проблеме, например:\n"
        '"У меня не работает компьютер"\n\n'
        "И я помогу тебе с блеском (ну, попытаюсь)! 😎"
    )
    await update.message.reply_text(welcome_text)

async def handle_problem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик сообщений о проблемах"""
    user_message = update.message.text.lower()
    
    # Проверяем, есть ли в сообщении ключевые слова о проблемах
    problem_keywords = [
        "не работает",
        "сломан",
        "ошибка",
        "не включается",
        "виснет",
        "тормозит",
        "не открывается",
        "проблема"
    ]
    
    if not any(keyword in user_message for keyword in problem_keywords):
        await update.message.reply_text(
            "Эй, ты мне о проблеме расскажи! Напиши что-то типа 'У меня не работает компьютер' 🤔"
        )
        return
    
    # Запрашиваем местоположение
    await update.message.chat.send_action(ChatAction.TYPING)
    location_request = (
        "🚨 ВНИМАНИЕ! ИНЦИДЕНТ ОБНАРУЖЕН! 🚨\n\n"
        "Окей, расскажи мне, ГДЕ ты сидишь?\n"
        "Например: 'Главный офис, этаж 2, стол 3'\n"
        "Или: 'Дома в спальне'\n\n"
        "Давай, не стесняйся! 📍"
    )
    await update.message.reply_text(location_request)
    
    # Сохраняем информацию в контексте
    context.user_data['has_problem'] = True
    context.user_data['problem_text'] = user_message

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ответа с местоположением"""
    
    # Проверяем, был ли запрос о местоположении
    if not context.user_data.get('has_problem'):
        await update.message.reply_text(
            "Сначала расскажи о своей проблеме! 🤨"
        )
        return
    
    location = update.message.text
    
    # Регистрируем запрос
    await update.message.chat.send_action(ChatAction.TYPING)
    
    registration_text = (
        f"✅ ЗАПРОС ЗАРЕГИСТРИРОВАН! ✅\n\n"
        f"📍 Локация: {location}\n"
        f"🔧 Проблема: {context.user_data['problem_text']}\n"
        f"🎫 Номер тикета: #{update.message.from_user.id}\n\n"
        f"Обрабатываю запрос... СТОЯЯААК... 🤖⚡"
    )
    await update.message.reply_text(registration_text)
    
    # Небольшая пауза для эффекта
    import asyncio
    await asyncio.sleep(random.randint(2, 4))
    
    # Отправляем смешное решение
    await update.message.chat.send_action(ChatAction.TYPING)
    solution = random.choice(ALL_SOLUTIONS)
    
    solution_text = (
        "💡 РЕШЕНИЕ НАЙДЕНО! 💡\n\n"
        f"{solution}\n\n"
        "Если не сработает - иди ныть в соседний отдел! 😄"
    )
    await update.message.reply_text(solution_text)
    
    # Очищаем контекст
    context.user_data.clear()

def main() -> None:
    """Запуск бота"""
    # Получай токен из переменной окружения или файла конфига
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        # Если нет переменной окружения, прочитай из файла config.py
        try:
            from config import TOKEN as CONFIG_TOKEN
            TOKEN = CONFIG_TOKEN
        except ImportError:
            logger.error("❌ ОШИБКА: Токен не найден!")
            logger.error("Установи переменную окружения TELEGRAM_BOT_TOKEN")
            logger.error("Или создай файл config.py с переменной TOKEN")
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    logger.info(f"✅ Токен найден: {TOKEN[:10]}...")
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    
    # Обработчик всех сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_problem))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location))
    
    # Запускаем бота
    logger.info("🤖 БОТ ЗАПУЩЕН! Жми Ctrl+C для остановки.")
    print("🤖 БОТ ЗАПУЩЕН! Жми Ctrl+C для остановки.")
    application.run_polling()

if __name__ == '__main__':
    main()
