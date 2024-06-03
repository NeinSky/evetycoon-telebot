from telebot.types import Message
from loader import bot, MINERALS, EMPIRES
from states.request_states import MarketOrderState
from keyboards import minerals, empires, security
from api.evetycoon import get_market_orders
from .constants import MESSAGE_MINERAL_CHOICE, MESSAGE_FILTER_CHOICE, MESSAGE_SYSTEM_FILTER, MESSAGE_MAY_TAKE_SOME_TIME


@bot.message_handler(commands=["wtb", "wts"])
def bot_start(message: Message):
    """Catches wtb and wts commands, sets orders' type and draws mineral filter buttons"""
    bot.set_state(message.from_user.id, MarketOrderState.order_type, message.chat.id)

    if 'wts' in message.text:
        order_type = 'wts'
    else:
        order_type = 'wtb'

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['order_type'] = order_type

    bot.set_state(message.from_user.id, MarketOrderState.mineral_id, message.chat.id)
    bot.send_message(
        message.from_user.id,
        MESSAGE_MINERAL_CHOICE,
        reply_markup=minerals.get_keyboard(),
    )


@bot.callback_query_handler(lambda query: query.data in MINERALS.keys(), state=MarketOrderState.mineral_id)
def set_mineral_filter(query):
    """Saves mineral's choice and draws empire filter buttons"""
    bot.set_state(
        query.from_user.id,
        MarketOrderState.empire_filter,
        query.message.chat.id
    )

    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as data:
        data['mineral_id'] = MINERALS[query.data][0]

    bot.send_message(
        query.from_user.id,
        MESSAGE_FILTER_CHOICE,
        reply_markup=empires.get_keyboard(),
    )


@bot.callback_query_handler(lambda query: query.data in EMPIRES.keys(), state=MarketOrderState.empire_filter)
def set_empire_filter(query):
    """Saves empire's choice and draws system security filter buttons"""
    bot.set_state(
        query.from_user.id,
        MarketOrderState.system_filter,
        query.message.chat.id
    )

    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as data:
        data['empire_filter'] = query.data

    bot.send_message(
        query.from_user.id,
        MESSAGE_SYSTEM_FILTER,
        reply_markup=security.get_keyboard(),
    )


@bot.callback_query_handler(lambda query: query.data in ['high', 'low', 'all'], state=MarketOrderState.system_filter)
def set_empire_security(query):
    """Saves systems' security filter, makes request and shows result"""
    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as data:
        data['system_filter'] = query.data
        data['user_id'] = query.from_user.id

    bot.send_message(
        query.from_user.id,
        MESSAGE_MAY_TAKE_SOME_TIME
    )

    bot.send_message(
        query.from_user.id,
        get_market_orders(data)
    )
