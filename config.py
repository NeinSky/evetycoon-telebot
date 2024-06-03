import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Environment was not loaded, because .env file was not found. Exiting.")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

BOT_COMMANDS = (
    ("start", "Start bot"),
    ("help", "Show commands and descriptions"),
    ("stats", "Market statistics by regions"),
    ("wtb", "Get sell orders"),
    ("wts", "Get buy orders"),
    ("history", "Show and repeat last requests"),
)

DB_NAME = 'evetycoonapi.db'
DB_ECHO_QUERY = True

NUM_OF_RESULTS = 5
