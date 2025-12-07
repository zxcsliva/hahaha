#!/bin/bash
# Скрипт для установки бота на PythonAnywhere

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Установка Telegram бота на PythonAnywhere${NC}"
echo -e "${GREEN}========================================${NC}"

# Шаг 1: Создание папки
echo -e "\n${YELLOW}[1/5] Создание папки...${NC}"
mkdir -p ~/telegram_bot
cd ~/telegram_bot
echo -e "${GREEN}✅ Папка создана${NC}"

# Шаг 2: Создание виртуального окружения
echo -e "\n${YELLOW}[2/5] Создание виртуального окружения...${NC}"
mkvirtualenv --python=/usr/bin/python3.10 telegram_bot
echo -e "${GREEN}✅ Виртуальное окружение создано${NC}"

# Шаг 3: Активация окружения и установка зависимостей
echo -e "\n${YELLOW}[3/5] Установка зависимостей...${NC}"
workon telegram_bot
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✅ Зависимости установлены${NC}"

# Шаг 4: Установка переменной окружения
echo -e "\n${YELLOW}[4/5] Настройка переменной окружения...${NC}"
read -p "Введи свой Telegram Bot Token: " BOT_TOKEN
echo "export TELEGRAM_BOT_TOKEN='$BOT_TOKEN'" >> ~/.bashrc
source ~/.bashrc
echo -e "${GREEN}✅ Токен установлен${NC}"

# Шаг 5: Проверка работы
echo -e "\n${YELLOW}[5/5] Проверка работы бота...${NC}"
timeout 5 python bot.py || true

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ УСТАНОВКА ЗАВЕРШЕНА!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Дальнейшие действия:${NC}"
echo -e "1. Перейди на https://www.pythonanywhere.com"
echo -e "2. Откройте раздел 'Tasks' → 'Always-on tasks'"
echo -e "3. Нажми 'Create a new always-on task'"
echo -e "4. Введи путь: /home/\$USER/.virtualenvs/telegram_bot/bin/python /home/\$USER/telegram_bot/bot.py"
echo -e "5. Нажми 'Create'"
echo -e "\n${GREEN}Готово! Бот работает 24/7!${NC}"
