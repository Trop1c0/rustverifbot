import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from py_components import (
    UI, Container, TextDisplay, Section, Separator, SeparatorSpacing,
    MediaGallery, ActionRow, Button, ButtonStyle, StringSelect, SelectOption
)

# Загрузка переменных окружения
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REGISTRATION_URL = os.getenv('REGISTRATION_URL')
ALLOWED_CHANNEL_ID = int(os.getenv('ALLOWED_CHANNEL_ID', '0'))

# Настройка intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Тексты на разных языках
TEXTS = {
    'en': {
        'choose_language': 'Please select your language',
        'language_name': 'English',
        'language_desc': 'Choose English language',
        'connecting': 'Connecting to servers',
        'please_wait': 'Please wait...',
        'connection_established': 'Connection established',
        'send_profile_link': 'Send link to your Clan table profile',
        'send_button': '✅ Send',
        'no_account': '❌ No account',
        'registration_required': 'Registration is required to access the server.',
        'go_to_registration': '✅ Go to registration'
    },
    'ru': {
        'choose_language': 'Please select your language',
        'language_name': 'Русский',
        'language_desc': 'Выбрать русский язык',
        'connecting': 'Подключение к серверам',
        'please_wait': 'Пожалуйста, подождите...',
        'connection_established': 'Подключение к серверам установлено',
        'send_profile_link': 'Отправьте ссылку на ваш профиль Clan table',
        'send_button': '✅ Отправить',
        'no_account': '❌ Нет аккаунта',
        'registration_required': 'Для доступа к серверу требуется регистрация.',
        'go_to_registration': '✅ Перейти к регистрации'
    },
    'fr': {
        'choose_language': 'Please select your language',
        'language_name': 'Français',
        'language_desc': 'Choisir la langue française',
        'connecting': 'Connexion aux serveurs',
        'please_wait': 'Veuillez patienter...',
        'connection_established': 'Connexion établie',
        'send_profile_link': 'Envoyez un lien vers votre profil Clan table',
        'send_button': '✅ Envoyer',
        'no_account': '❌ Pas de compte',
        'registration_required': "L'inscription est requise pour accéder au serveur.",
        'go_to_registration': "✅ Aller à l'inscription"
    },
    'es': {
        'choose_language': 'Please select your language',
        'language_name': 'Español',
        'language_desc': 'Elige el idioma español',
        'connecting': 'Conectando a servidores',
        'please_wait': 'Por favor espere...',
        'connection_established': 'Conexión establecida',
        'send_profile_link': 'Envíe un enlace a su perfil de Clan table',
        'send_button': '✅ Enviar',
        'no_account': '❌ No hay cuenta',
        'registration_required': 'Se requiere registro para acceder al servidor.',
        'go_to_registration': '✅ Ir a registro'
    }
}

# Хранилище выбранных языков пользователей
user_languages = {}

# Глобальный registry для обработки взаимодействий
from py_components import Registry
component_registry = Registry()

@component_registry.route("language_select")
async def handle_language_select(interaction: discord.Interaction):
    lang = interaction.data['values'][0]
    user_languages[interaction.user.id] = lang
    texts = TEXTS[lang]
    
    # Показываем "Подключение к серверам"
    ui = create_connecting_ui(texts)
    payload = ui.to_payload()
    
    # Используем низкоуровневый метод редактирования
    from py_components import edit_message
    await interaction.response.defer()
    await edit_message(
        interaction.channel_id,
        interaction.message.id,
        bot.http.token,
        payload
    )
    
    # Имитация подключения
    await asyncio.sleep(2)
    
    # Показываем успешное подключение
    ui = create_profile_ui(texts, lang)
    payload = ui.to_payload()
    await edit_message(
        interaction.channel_id,
        interaction.message.id,
        bot.http.token,
        payload
    )

@component_registry.route("send_profile")
async def handle_send_profile(interaction: discord.Interaction):
    lang = user_languages.get(interaction.user.id, 'ru')
    texts = TEXTS[lang]
    await interaction.response.send_message(
        texts['send_profile_link'],
        ephemeral=True
    )

@component_registry.route("no_account")
async def handle_no_account(interaction: discord.Interaction):
    lang = user_languages.get(interaction.user.id, 'ru')
    texts = TEXTS[lang]
    ui = create_registration_ui(texts, lang)
    payload = ui.to_payload()
    
    # Используем низкоуровневый метод редактирования
    from py_components import edit_message
    await interaction.response.defer()
    await edit_message(
        interaction.channel_id,
        interaction.message.id,
        bot.http.token,
        payload
    )

def create_language_select_ui():
    """Создает начальное сообщение с выбором языка"""
    image_path = os.path.join('assets', 'image.jpg')
    
    ui = UI(
        Container(
            MediaGallery(f"attachment://image.jpg"),
            Separator(spacing=SeparatorSpacing.SMALL),
            TextDisplay("# Rust Clan Table"),
            Separator(divider=False, spacing=SeparatorSpacing.SMALL),
            TextDisplay("Please select your language"),
            Separator(spacing=SeparatorSpacing.SMALL),
        ),
        ActionRow(
            StringSelect(
                "language_select",
                options=[
                    SelectOption("English", "en", description="Choose English language", emoji="🇬🇧"),
                    SelectOption("Русский", "ru", description="Выбрать русский язык", emoji="🇷🇺"),
                    SelectOption("Français", "fr", description="Choisir la langue française", emoji="🇫🇷"),
                    SelectOption("Español", "es", description="Elige el idioma español", emoji="🇪🇸"),
                ],
                placeholder="Select language...",
            )
        ),
    )
    
    return ui

def create_connecting_ui(texts):
    """Создает сообщение с индикацией подключения"""
    ui = UI(
        Container(
            MediaGallery(f"attachment://image.jpg"),
            Separator(spacing=SeparatorSpacing.SMALL),
            TextDisplay(f"# ⏳ {texts['connecting']}"),
            Separator(divider=False, spacing=SeparatorSpacing.SMALL),
            TextDisplay(texts['please_wait']),
        ),
    )
    return ui

def create_profile_ui(texts, lang):
    """Создает сообщение с запросом профиля"""
    ui = UI(
        Container(
            MediaGallery(f"attachment://image.jpg"),
            Separator(spacing=SeparatorSpacing.SMALL),
            TextDisplay(f"# ✅ {texts['connection_established']}"),
            Separator(divider=False, spacing=SeparatorSpacing.SMALL),
            TextDisplay(f"ℹ️ {texts['send_profile_link']}"),
        ),
        Button(texts['send_button'], custom_id='send_profile', style=ButtonStyle.SUCCESS),
        Button(texts['no_account'], custom_id='no_account', style=ButtonStyle.DANGER),
    )
    return ui

def create_registration_ui(texts, lang):
    """Создает сообщение с кнопкой регистрации"""
    ui = UI(
        Container(
            MediaGallery(f"attachment://image.jpg"),
            Separator(spacing=SeparatorSpacing.SMALL),
            TextDisplay("# Rust Clan Table"),
            Separator(divider=False, spacing=SeparatorSpacing.SMALL),
            TextDisplay(f"ℹ️ {texts['registration_required']}"),
        ),
        Button(texts['go_to_registration'], style=ButtonStyle.LINK, url=REGISTRATION_URL, emoji='🔗'),
    )
    return ui

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')
    print(f'ID: {bot.user.id}')
    print('Попытка синхронизации команд...')
    try:
        synced = await bot.tree.sync()
        print(f'✅ Синхронизировано {len(synced)} команд:')
        for cmd in synced:
            print(f'  - /{cmd.name}')
    except Exception as e:
        print(f'❌ Ошибка синхронизации команд: {e}')
        import traceback
        traceback.print_exc()
    print('------')
    print('Бот готов к работе!')
    print(f'Пригласите бота с правами: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=274877991936&scope=bot%20applications.commands')

@bot.event
async def on_interaction(interaction):
    """Обработка всех взаимодействий с компонентами"""
    if interaction.type.name == "component":
        custom_id = interaction.data.get("custom_id")
        if custom_id:
            await component_registry.dispatch(custom_id, interaction)

@bot.tree.command(name='rust', description='Запустить верификацию для пользователя')
@app_commands.describe(member='Выберите пользователя для верификации')
async def rust(interaction: discord.Interaction, member: discord.Member):
    """Slash команда для запуска верификации конкретного пользователя"""
    
    # Проверка канала
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            "Пошел нахуй",
            ephemeral=True
        )
        return
    
    image_path = os.path.join('assets', 'image.jpg')
    
    try:
        # Создаем UI с Components V2
        ui = create_language_select_ui()
        
        # Отправляем в личку пользователю
        if os.path.exists(image_path):
            file = discord.File(image_path, filename='image.jpg')
            await ui.send(member, files=[{"fp": file.fp, "filename": "image.jpg", "content_type": "image/jpeg"}])
        else:
            await ui.send(member)
        
        # Подтверждение в канале
        await interaction.response.send_message(
            f"✅ Сообщение отправлено {member.mention} в личные сообщения",
            ephemeral=True
        )
    except discord.Forbidden:
        # Если у пользователя закрыты ЛС
        await interaction.response.send_message(
            f"❌ Не могу отправить сообщение {member.mention}. У пользователя закрыты личные сообщения.",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Ошибка при отправке сообщения: {e}",
            ephemeral=True
        )

@bot.event
async def on_message(message):
    # Игнорируем сообщения от ботов
    if message.author.bot:
        return
    
    # Обрабатываем команды
    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
