from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard(num_of_buttons: int) -> InlineKeyboardMarkup:
    """Returns inline keyboard markup of history buttons"""
    buttons = [InlineKeyboardButton(text=str(i_key), callback_data=str(i_key))
               for i_key in range(1, num_of_buttons+1)]

    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard
