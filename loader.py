from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
import config
from os.path import exists
from database.connection import engine
from database.models import Base
from database.static_data import load_static_data
from utils.set_commands import set_commands
from database.models import Mineral, Empire, Region

if not exists(config.DB_NAME):
    Base.metadata.create_all(bind=engine)
load_static_data()

# pre-load static data
MINERALS: dict[str: tuple[int, str]] = Mineral.get_minerals_short_name()
EMPIRES: dict[str: tuple[int, str]] = Empire.get_empires()
EMPIRE_REGIONS: dict[list[tuple]] = Region.get_empire_regions()
REGIONS_ID_TO_NAMES: dict[int: str] = Region.get_region_id_to_name()
MINERALS_ID_TO_SHORT_NAME: dict[int: str] = Mineral.mineral_id_to_short_name()

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
set_commands(bot)
bot.add_custom_filter(custom_filters.StateFilter(bot))
