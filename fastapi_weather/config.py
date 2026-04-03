from os import getenv
from dotenv import load_dotenv

load_dotenv()

WEATHER_TOKEN = getenv("API_TOKEN")
