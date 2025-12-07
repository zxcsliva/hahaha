#!/usr/bin/env python3
"""
🤖 ЛЕГЕНДАРНЫЙ БОТ ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ 🤖
Смешной Telegram бот с 600+ вариантами ответов
"""

import logging
import random
import os
import asyncio
import json
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.constants import ChatAction
from solutions import ALL_SOLUTIONS

# Состояния диалога
WAITING_FOR_LOCATION = 1
WAITING_FOR_NEW_ANSWER = 2
WAITING_FOR_ANSWER_CONFIRM = 3

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

# Файлы для хранения данных
CUSTOM_ANSWERS_FILE = 'custom_answers.json'
AUTHORS_FILE = 'authors.json'

def load_custom_answers():
    """Загружает пользовательские ответы из файла"""
    try:
        if os.path.exists(CUSTOM_ANSWERS_FILE):
            with open(CUSTOM_ANSWERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка при загрузке пользовательских ответов: {e}")
    return []

def load_authors():
    """Загружает авторов решений"""
    try:
        if os.path.exists(AUTHORS_FILE):
            with open(AUTHORS_FILE, 'r', encoding='utf-8') as f:
                authors = json.load(f)
                logger.info(f"✅ Загружено {len(authors)} авторов из {AUTHORS_FILE}")
                return authors
        else:
            logger.warning(f"⚠️ Файл {AUTHORS_FILE} не найден в {os.getcwd()}")
    except Exception as e:
        logger.error(f"Ошибка при загрузке авторов: {e}")
    
    logger.info("Используется дефолтный автор: Аноним Безымянов")
    return ["Аноним Безымянов"]

def save_custom_answers(answers):
    """Сохраняет пользовательские ответы в файл"""
    try:
        with open(CUSTOM_ANSWERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(answers, f, ensure_ascii=False, indent=2)
        logger.info(f"Сохранено {len(answers)} пользовательских ответов")
    except Exception as e:
        logger.error(f"Ошибка при сохранении ответов: {e}")

# Загружаем данные при старте
CUSTOM_ANSWERS = load_custom_answers()
AUTHORS = load_authors()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_text = (
        "🤖 ЙО, ДОБРО ПОЖАЛОВАТЬ В ТЕХПОДДЕРЖКУ! 🤖\n\n"
        "Я - ЛЕГЕНДАРНЫЙ БОТ ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ!\n"
        "Просто напиши мне о своей проблеме, например:\n"
        '"У меня не работает компьютер"\n\n'
        "Команды:\n"
        "/add_answer - добавить свой смешный ответ\n"
        "/stats - статистика ответов\n"
        "/help - помощь\n\n"
        "И я помогу тебе с блеском (ну, попытаюсь)! 😎"
    )
    await update.message.reply_text(welcome_text)


async def add_answer_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало процесса добавления нового ответа"""
    await update.message.reply_text(
        "📝 ДОБАВЛЕНИЕ НОВОГО СМЕШНОГО ОТВЕТА\n\n"
        "Напиши смешной ответ который должен дать бот в качестве решения:\n"
        "(Можно использовать эмодзи и форматирование)\n\n"
        "Пример: 'Выключи это и включи обратно, гений! 🤦'"
    )
    return WAITING_FOR_NEW_ANSWER


async def get_new_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получение нового ответа"""
    new_answer = update.message.text
    context.user_data['new_answer'] = new_answer
    
    await update.message.reply_text(
        f"✅ Вот что я получил:\n\n"
        f'"{new_answer}"\n\n'
        f"Это правильно? Напиши 'да' чтобы добавить или 'отмена' чтобы отменить"
    )
    return WAITING_FOR_ANSWER_CONFIRM


async def confirm_new_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Подтверждение нового ответа"""
    response = update.message.text.lower().strip()
    
    if response == 'да':
        new_answer = context.user_data['new_answer']
        
        # Добавляем в оперативную память
        ALL_SOLUTIONS.append(new_answer)
        CUSTOM_ANSWERS.append(new_answer)
        
        # Сохраняем в файл
        save_custom_answers(CUSTOM_ANSWERS)
        
        await update.message.reply_text(
            f"🎉 ОТВЕТ ДОБАВЛЕН!\n\n"
            f"Теперь у бота {len(ALL_SOLUTIONS)} вариантов ответов!\n"
            f"Твой ответ будет использоваться в решениях! 😎\n\n"
            f"Можешь написать мне еще про проблему или добавить еще ответ (/add_answer)"
        )
    else:
        await update.message.reply_text(
            "❌ Добавление отменено.\n\n"
            "Напиши мне про проблему или используй /add_answer чтобы добавить другой ответ"
        )
    
    context.user_data.clear()
    return ConversationHandler.END


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает статистику"""
    total = len(ALL_SOLUTIONS)
    custom = len(CUSTOM_ANSWERS)
    built_in = total - custom
    
    stats_text = (
        f"📊 СТАТИСТИКА ОТВЕТОВ\n\n"
        f"Всего ответов: {total}\n"
        f"├─ Встроенных: {built_in}\n"
        f"└─ Добавлено пользователями: {custom}\n\n"
        f"Каждый раз бот случайно выбирает один из {total} вариантов! 🎲"
    )
    
    if CUSTOM_ANSWERS:
        stats_text += f"\n\n📝 ПОСЛЕДНИЕ ТВОИ ОТВЕТЫ:\n"
        for i, answer in enumerate(CUSTOM_ANSWERS[-5:], 1):  # Показываем последние 5
            stats_text += f"{i}. {answer[:50]}...\n" if len(answer) > 50 else f"{i}. {answer}\n"
    
    await update.message.reply_text(stats_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Помощь"""
    help_text = (
        "🆘 ПОМОЩЬ\n\n"
        "Как пользоваться ботом:\n\n"
        "1️⃣ Напиши о проблеме:\n"
        "   'У меня не работает компьютер'\n"
        "   'Монитор не включается'\n"
        "   'Ноутбук виснет'\n\n"
        "2️⃣ Бот спросит где ты сидишь\n\n"
        "3️⃣ Ответь локацией:\n"
        "   'Офис, этаж 2, стол 3'\n"
        "   'Дома в спальне'\n\n"
        "4️⃣ Получи смешное решение! 😂\n\n"
        "Команды:\n"
        "/start - начало\n"
        "/add_answer - добавить свой ответ\n"
        "/stats - статистика\n"
        "/help - эта помощь"
    )
    await update.message.reply_text(help_text)


async def handle_problem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик сообщений о проблемах"""
    user_message = update.message.text.lower()
    
    # Ключевые слова для обнаружения проблемы
    problem_keywords = ['не работает', 'сломан', 'ошибка', 'глюк', 'криво', 'проблема', 'багован', 'упал', 'повис', 'не включ', 'не открыв', 'не загружается']
    
    # Проверяем наличие ключевых слов
    has_problem = any(keyword in user_message for keyword in problem_keywords)
    
    if has_problem:
        # Сохраняем текст проблемы
        context.user_data['problem_text'] = update.message.text
        
        # Отправляем уведомление о проблеме
        await update.message.reply_text(
            "🚨 ИНЦИДЕНТ ОБНАРУЖЕН! 🚨\n\n"
            "Дай-ка я уточню... Где именно ты сидишь?\n"
            "Скажи локацию, например: 'Главный офис, этаж 2, стол 3'"
        )
        
        # Переходим в состояние ожидания локации
        return WAITING_FOR_LOCATION
    else:
        # Если это не проблема, отправляем стандартное сообщение
        await update.message.reply_text(
            "Эй! 👋\n\n"
            "Это похоже не на проблему с компьютером...\n"
            "Расскажи мне о своей беде! 😅\n\n"
            "Или используй /add_answer чтобы добавить смешный ответ"
        )
        return None


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик сообщения о локации"""
    location = update.message.text
    problem_text = context.user_data.get('problem_text', 'Неизвестная проблема')
    
    # Показываем статус обработки
    await update.message.chat.send_action(ChatAction.TYPING)
    
    # Регистрируем запрос
    registration_text = (
        "✅ ЗАПРОС ЗАРЕГИСТРИРОВАН! ✅\n\n"
        f"📍 Локация: {location}\n"
        f"🔧 Проблема: {problem_text}\n"
        f"🎫 Номер тикета: #{update.message.from_user.id}\n\n"
        "Обрабатываю запрос... СТОЯЯААК... 🤖⚡"
    )
    await update.message.reply_text(registration_text)
    
    # Небольшая пауза для драматизма
    await asyncio.sleep(2)
    
    # Выбираем случайное решение (включая пользовательские)
    solution = random.choice(ALL_SOLUTIONS)
    author = random.choice(AUTHORS)
    
    solution_text = (
        "💡 РЕШЕНИЕ НАЙДЕНО! 💡\n\n"
        f"{solution}\n\n"
        "─────────────────────\n"
        f"✍️ Автор решения: {author}\n"
        "─────────────────────\n\n"
        "Спасибо что обратился! До новых встреч! 😎\n\n"
        "Хочешь добавить свой смешной ответ? /add_answer"
    )
    await update.message.reply_text(solution_text)
    
    # Очищаем данные пользователя
    context.user_data.clear()
    
    # Возвращаемся в начальное состояние
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена диалога"""
    await update.message.reply_text(
        "❌ Диалог отменен.\n\n"
        "Напиши что-нибудь еще! 👋"
    )
    context.user_data.clear()
    return ConversationHandler.END


async def main():
    """Главная функция - БОТ СТАРТУЕТ ОТСЮДА"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("❌ ОШИБКА: Переменная окружения TELEGRAM_BOT_TOKEN не установлена!")
        return
    
    logger.info(f"✅ Токен найден. Всего ответов: {len(ALL_SOLUTIONS)}")
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Обработчик состояний для добавления ответов
    add_answer_handler = ConversationHandler(
        entry_points=[CommandHandler('add_answer', add_answer_start)],
        states={
            WAITING_FOR_NEW_ANSWER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_new_answer)
            ],
            WAITING_FOR_ANSWER_CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_new_answer)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Обработчик состояний для основного диалога (проблема -> локация)
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_problem)],
        states={
            WAITING_FOR_LOCATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", show_stats))
    application.add_handler(add_answer_handler)
    application.add_handler(conv_handler)
    
    logger.info("🤖 БОТ ЗАПУЩЕН! Жди сообщений...")
    
    # Инициализируем и запускаем
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    # Блокируем выполнение на вечно (пока бот не будет остановлен)
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
        await application.stop()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await application.stop()


if __name__ == '__main__':
    # Проверяем есть ли уже running loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Нет running loop - создаем новый
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Запускаем main как task
    try:
        loop.run_until_complete(main())
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            # На PythonAnywhere loop уже работает, просто создаем task
            asyncio.ensure_future(main())
        else:
            raise
