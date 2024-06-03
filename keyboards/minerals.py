from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import MINERALS


def get_keyboard() -> InlineKeyboardMarkup:
    """Returns inline keyboard markup of mineral filter buttons"""
    buttons = []
    for name, data in MINERALS.items():
        buttons.append(
            InlineKeyboardButton(text=data[1], callback_data=name)
        )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard
