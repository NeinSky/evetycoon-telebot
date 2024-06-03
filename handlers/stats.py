from telebot.types import Message
from loader import bot, MINERALS, EMPIRES
from states.request_states import MarketStatsState
from keyboards import minerals, empires
from api.evetycoon import get_market_stats
from .constants import MESSAGE_MINERAL_CHOICE, MESSAGE_FILTER_CHOICE, MESSAGE_MAY_TAKE_SOME_TIME


@bot.message_handler(commands=["stats"])
def bot_start(message: Message):
    """Catches stats command and draws mineral filter buttons"""
    bot.set_state(message.from_user.id, MarketStatsState.mineral_id, message.chat.id)
    bot.send_message(
        message.from_user.id,
        MESSAGE_MINERAL_CHOICE,
        reply_markup=minerals.get_keyboard(),
    )


@bot.callback_query_handler(lambda query: query.data in MINERALS.keys(), state=MarketStatsState.mineral_id)
def set_mineral_filter(query):
    """Saves mineral's choice and draws empire filter buttons"""
    bot.set_state(
        query.from_user.id,
        MarketStatsState.empire_filter,
        query.message.chat.id
    )
    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as data:
        data['mineral_id'] = MINERALS[query.data][0]

    bot.send_message(
        query.from_user.id,
        MESSAGE_FILTER_CHOICE,
        reply_markup=empires.get_keyboard(),
    )


@bot.callback_query_handler(lambda query: query.data in EMPIRES.keys(), state=MarketStatsState.empire_filter)
def set_empire_filter(query):
    """Saves empire's choice, makes requests and shows result"""
    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as data:
        data['empire_filter'] = query.data
        data['user_id'] = query.from_user.id

    bot.send_message(
        query.from_user.id,
        MESSAGE_MAY_TAKE_SOME_TIME
    )

    bot.send_message(
        query.from_user.id,
        get_market_stats(data)
    )
