#python3
import paramiko
import re
import asyncio
from telegram import Bot

# При использовании python выше версии 3.8 библиотека telegram  может не работать тогда вам нужно "pip unistall telegram" и вместо этого сделать
# pip install python-telegram-bot
async def send_message(chat_id, telegram_message, bot_token):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=telegram_message)
# List of words to search for
words_to_search = ['WARNING','ERROR','ls -la' ] #Вы можете добавить любые слова для поиска в ваших логах

# The log file to analyze on the remote system
log_file = '/dir/log/logfile.log'

# Connect to the remote system
hostname = "хост"
username = "имя пользователя"
password = "пароль"
port = "порт"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(hostname=hostname, username=username, password=password, port=port)
except Exception as e:
    print(f'Error  SSH connection: {e}')

# Read the log file on the remote system
stdin, stdout, stderr = ssh.exec_command(f"cat {log_file}")
log_lines = stdout.readlines()

# Search for each word in the log file
telegram_message = "Warn: "

# Iterate through the words
for word in words_to_search:
    for i, line in enumerate(log_lines):
        match = re.search(word, line)
        if match:
            telegram_message += f'{word} found in {i} : {line}. '


if telegram_message != "Warn: ":
    try:
        # Telegram bot details
        bot_token = "ВАШ ТОКЕН БОТА"
        chat_id = "ЧАТ ИД"

        # Send message to Telegram
        message_chunks = [telegram_message[i:i+4096] for i in range(0, len(telegram_message), 4096)]
        for message in message_chunks:
            asyncio.run(send_message(chat_id, message, bot_token))

        print(f'Telegram messages sent to chat id {chat_id}')
    except Exception as e:
        print(f'Error sending Telegram message: {e}')

try:
    # Close the SSH connection
    ssh.close()
except Exception as e:
    print(f'Error closing SSH connection: {e}')
