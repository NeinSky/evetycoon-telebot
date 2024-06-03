from telebot.types import Message
from loader import bot, MINERALS_ID_TO_SHORT_NAME
from database.models import Request
from keyboards import numeric
from .constants import MESSAGE_NO_REQUESTS_FOUND, MESSAGE_HISTORY_WRONG_REQUEST, MESSAGE_MAY_TAKE_SOME_TIME
from states.request_states import HistoryState
from api.evetycoon import get_market_orders, get_market_stats

LAST_REQUESTS = []


def _get_message(data: list) -> str:
    msg = 'Request history:\n\n'
    counter = 1
    for row in data:
        cmd = row[0].split(';')
        command = cmd[0]
        mineral = MINERALS_ID_TO_SHORT_NAME[int(cmd[1])]
        empire = cmd[2]
        security = cmd[3] if command in ['wtb', 'wts'] else ''

        msg += f'{counter}. {row[1]}: {command} {mineral} {empire} {security}\n'
        counter += 1
    return msg


@bot.message_handler(commands=["history"])
def bot_help(message: Message):
    """Shows user's request history (if any)"""
    bot.set_state(message.from_user.id, HistoryState.cmd_choice, message.chat.id)

    global LAST_REQUESTS
    LAST_REQUESTS = Request.get_users_last_requests(message.from_user.id)
    msg = _get_message(LAST_REQUESTS)

    if LAST_REQUESTS:
        bot.send_message(
            message.from_user.id,
            msg,
            reply_markup=numeric.get_keyboard(len(LAST_REQUESTS))
        )
    else:
        bot.send_message(message.from_user.id, MESSAGE_NO_REQUESTS_FOUND)


@bot.callback_query_handler(lambda query: True, state=HistoryState.cmd_choice)
def repeat_cmd(query):
    """Repeats chosen request"""

    # check if choice is a number and between zero and LAST_REQUEST len-1
    if query.data.isnumeric() and (1 <= int(query.data) <= len(LAST_REQUESTS)):
        request = LAST_REQUESTS[int(query.data)-1][0].split(';')
        data = {
            'mineral_id': request[1],
            'empire_filter': request[2],
            'user_id': query.from_user.id,
        }
        bot.send_message(query.from_user.id, MESSAGE_MAY_TAKE_SOME_TIME)
        if request[0] == 'stats':
            bot.send_message(query.from_user.id, get_market_stats(data))
        elif request[0] in ['wtb', 'wts']:
            data['order_type'] = request[0]
            data['system_filter'] = request[3]
            bot.send_message(query.from_user.id, get_market_orders(data))
        else:
            bot.send_message(query.from_user.id, MESSAGE_HISTORY_WRONG_REQUEST)
    else:
        bot.send_message(query.from_user.id, MESSAGE_HISTORY_WRONG_REQUEST)
