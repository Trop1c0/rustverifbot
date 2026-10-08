# Rust Verification Bot (Discord)

Discord бот для верификации игроков Rust через Clan Table.

## Возможности

- 🌍 Мультиязычность (English, Русский, Français, Español)
- 🎨 Красивый интерфейс с embed сообщениями и изображениями
- 🔗 Интеграция с системой регистрации Rust Clan Table
- ✅ Верификация через профиль Clan Table
- 📨 Отправка сообщений в личку пользователя

## Установка на Ubuntu 20.04

### 1. Обновление системы и установка Python
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

### 2. Клонирование репозитория
```bash
git clone https://github.com/YOUR_USERNAME/rustverifbot.git
cd rustverifbot
```

### 3. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка .env файла
```bash
cp .env.example .env
nano .env
```

Укажите:
- `DISCORD_TOKEN` - токен вашего Discord бота
- `REGISTRATION_URL` - ссылка на регистрацию

### 6. Запуск бота
```bash
python3 bot.py
```

## Запуск в фоне с помощью systemd

### 1. Создайте systemd service файл
```bash
sudo nano /etc/systemd/system/rustverifbot.service
```

### 2. Вставьте конфигурацию (замените YOUR_USER на ваше имя пользователя):
```ini
[Unit]
Description=Rust Verification Discord Bot
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/home/YOUR_USER/rustverifbot
ExecStart=/home/YOUR_USER/rustverifbot/venv/bin/python3 /home/YOUR_USER/rustverifbot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Запустите сервис
```bash
sudo systemctl daemon-reload
sudo systemctl enable rustverifbot
sudo systemctl start rustverifbot
```

### 4. Проверка статуса
```bash
sudo systemctl status rustverifbot
```

### Полезные команды
- Остановить бота: `sudo systemctl stop rustverifbot`
- Перезапустить бота: `sudo systemctl restart rustverifbot`
- Логи: `sudo journalctl -u rustverifbot -f`

## Использование

Используй slash команду:
```
/rust @member
```

Бот отправит сообщение пользователю в личку с выбором языка и процессом верификации.

## Структура

```
rustverifbot/
├── bot.py              # Discord бот
├── requirements.txt    # discord.py
├── .env               # Токен и настройки (не в git)
├── .env.example       # Пример настроек
├── assets/
│   └── image.jpg      # Картинка Rust Clan Table
└── README.md
```

## Получение Discord токена

1. Перейдите на https://discord.com/developers/applications
2. Создайте новое приложение
3. Перейдите в раздел "Bot"
4. Скопируйте токен
5. В разделе "OAuth2 > URL Generator" выберите:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`
6. Используйте сгенерированную ссылку для добавления бота на сервер
