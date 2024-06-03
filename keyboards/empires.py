from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import EMPIRES


def get_keyboard() -> InlineKeyboardMarkup:
    """Returns inline keyboard markup of empire filter buttons"""
    buttons = []
    for name, data in EMPIRES.items():
        buttons.append(
            InlineKeyboardButton(text=name, callback_data=name)
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard
