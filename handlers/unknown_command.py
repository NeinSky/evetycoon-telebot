from telebot.types import Message
from loader import bot
from .constants import MESSAGE_UNKNOWN_COMMAND


@bot.message_handler()
def handle_unknown_command(message: Message):
    """Handles unknown command"""
    bot.send_message(
        message.from_user.id,
        MESSAGE_UNKNOWN_COMMAND
    )
