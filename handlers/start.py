from telebot.types import Message
from loader import bot
from .constants import MESSAGE_START


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """Returns welcome message with command list"""
    bot.reply_to(message, MESSAGE_START.format(user=message.from_user.full_name))
