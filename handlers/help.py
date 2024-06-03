from telebot.types import Message

from config import BOT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """Shows list of commands and their description"""
    text = [f"/{command} - {desc}" for command, desc in BOT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
