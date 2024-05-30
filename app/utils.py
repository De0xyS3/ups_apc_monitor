import platform
import subprocess
from pysnmp.hlapi import *
import telegram
import paramiko
import time
import asyncio


def ping_host(ip):
    """
    Returns True if host responds to a ping request, False otherwise.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        return '1 received' in output
    except subprocess.CalledProcessError:
        return False


async def send_telegram_message_async(message):
    bot = telegram.Bot(token='your_token')
    chat_id = 'your_id'  # Puedes obtener el chat_id usando el bot @userinfobot
    await bot.send_message(chat_id=chat_id, text=message)

def send_telegram_message_sync(message):
    asyncio.run(send_telegram_message_async(message))

def send_telegram_message(message):
    send_telegram_message_sync(message)

