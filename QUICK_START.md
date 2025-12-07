# 📖 БЫСТРЫЙ СТАРТ - РАЗВЕРТЫВАНИЕ НА PYTHONANYWHERE

## ⚡ 5 МИНУТ ДО ЗАПУСКА БОТА

### 1️⃣ Логин + Bash
```
https://www.pythonanywhere.com → Bash console
```

### 2️⃣ Загрузка файлов
```bash
cd ~
mkdir telegram_bot
cd telegram_bot
# Загрузи файлы через Files интерфейс ИЛИ Git
```

### 3️⃣ Установка (копируй-паста)
```bash
mkvirtualenv --python=/usr/bin/python3.10 telegram_bot
workon telegram_bot
pip install -r requirements.txt
```

### 4️⃣ Установка токена
```bash
echo "export TELEGRAM_BOT_TOKEN='твой_токен_от_BotFather'" >> ~/.bashrc
source ~/.bashrc
```

### 5️⃣ Проверка
```bash
python bot.py
# Должно вывести: "🤖 БОТ ЗАПУЩЕН!"
# Нажми Ctrl+C
```

### 6️⃣ Always-On Task (ГЛАВНОЕ!)
1. Нажми "Tasks" в левом меню
2. "Create a new always-on task"
3. Вставь:
```
/home/username/.virtualenvs/telegram_bot/bin/python /home/username/telegram_bot/bot.py
```
4. Замени `username` на свой username
5. "Create"
6. Готово! 🟢 GREEN = БОТ РАБОТАЕТ!

### 7️⃣ Тест в Telegram
- Откройте Telegram
- Найди своего бота
- Напиши: "У меня не работает компьютер"
- Получи смешный ответ ✅

---

## 🆘 ПРОБЛЕМЫ?

| Проблема | Решение |
|----------|---------|
| Модуль не найден | `pip install -r requirements.txt` |
| Токен не установлен | `echo "export TELEGRAM_BOT_TOKEN='ТОКЕН'" >> ~/.bashrc; source ~/.bashrc` |
| Бот не отвечает | Перезагрузи task: Tasks → Restart |
| Memory issues | Удали логи: `rm ~/telegram_bot/*.log` |

---

## 📚 ПОЛНАЯ ИНСТРУКЦИЯ

Смотри файл **`PYTHONANYWHERE_GUIDE.md`**

---

## ✅ ГОТОВО!

Твой бот работает 24/7! 🎉
