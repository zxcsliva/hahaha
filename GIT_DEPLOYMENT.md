# 🚀 РАЗВЕРТЫВАНИЕ ЧЕРЕЗ GIT

## Если у тебя есть GitHub репозиторий

### 1. Подготовка репозитория на GitHub

1. Создай новый репозиторий на GitHub
2. Загрузи туда файлы:
   - `bot.py`
   - `solutions.py`
   - `requirements.txt`
   - `config.py`
3. НЕ загружай файл с токеном!

**Рекомендуемая структура репозитория:**

```
telegram-bot/
├── bot.py
├── solutions.py
├── requirements.txt
├── config.py
├── .gitignore
├── README.md
└── .env.example
```

### 2. Файл .gitignore

Создай файл `.gitignore` чтобы не загружал чувствительные файлы:

```
# Логи
*.log
bot.log

# Config с токеном
config.py

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env
```

### 3. Файл .env.example

Создай пример файла переменных окружения:

```
TELEGRAM_BOT_TOKEN=ТВО_ТОКЕН_ЗДЕСЬ
DEBUG=False
```

### 4. На PythonAnywhere - Bash команда

```bash
cd ~
mkdir telegram_bot
cd telegram_bot
git clone https://github.com/твой_username/telegram-bot.git .
mkvirtualenv --python=/usr/bin/python3.10 telegram_bot
workon telegram_bot
pip install -r requirements.txt
echo "export TELEGRAM_BOT_TOKEN='твой_токен'" >> ~/.bashrc
source ~/.bashrc
python bot.py  # Проверка
```

---

## Альтернатива: Загрузить ZIP

### 1. Скачай файлы с GitHub

GitHub → "Code" → "Download ZIP"

### 2. На PythonAnywhere

В Bash консоли:

```bash
cd ~
mkdir telegram_bot
cd telegram_bot
```

Потом в веб-интерфейсе:
- Нажми "Files"
- Перейди в папку telegram_bot
- Нажми "Upload a file"
- Выбери скачанный ZIP
- Нажми "Extract here"

### 3. Установка

```bash
cd ~/telegram_bot
mkvirtualenv --python=/usr/bin/python3.10 telegram_bot
workon telegram_bot
pip install -r requirements.txt
echo "export TELEGRAM_BOT_TOKEN='твой_токен'" >> ~/.bashrc
source ~/.bashrc
```

---

## Преимущества Git способа

✅ Легко обновлять код (просто `git pull`)
✅ История изменений
✅ Легко работать с несколькими версиями
✅ Профессионально выглядит

## Требует

❌ Знание Git/GitHub (но базовое достаточно)
❌ Создание GitHub аккаунта (бесплатно)
