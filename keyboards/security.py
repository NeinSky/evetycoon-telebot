from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard() -> InlineKeyboardMarkup:
    """Returns inline keyboard markup of systems security filter buttons"""
    buttons = [
        InlineKeyboardButton(text='HIGHSEC', callback_data='high'),
        InlineKeyboardButton(text='LOWSEC', callback_data='low'),
        InlineKeyboardButton(text='All', callback_data='all'),
    ]

    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard
