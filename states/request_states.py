from telebot.handler_backends import State, StatesGroup


class MarketStatsState(StatesGroup):
    mineral_id = State()
    empire_filter = State()


class MarketOrderState(StatesGroup):
    order_type = State()
    mineral_id = State()
    empire_filter = State()
    system_filter = State()


class HistoryState(StatesGroup):
    cmd_choice = State()
