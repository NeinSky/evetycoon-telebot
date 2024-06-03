from telebot.types import BotCommand
from config import BOT_COMMANDS


def set_commands(bot):
    bot.set_my_commands(
        [BotCommand(*cmd) for cmd in BOT_COMMANDS]
    )
