from .config import WEATHER_TOKEN
from requests import get
from datetime import datetime
from typing import Any


def get_weather_now_func() -> dict[str, Any]:
    """Получает текущую погоду в Москве в виде json и отдает в python объекте."""

    raw_data = get(f'http://api.weatherapi.com/v1/current.json?key={WEATHER_TOKEN}&q=Moscow&aqi=no&alerts=no&lang=ru').json()
    return raw_data

def formatted_weather_data(raw_data: dict) -> dict[str, Any]:
    """Принимает сырые данные и отдаёт нужные строки в отформатированном формате."""

    day = datetime.strptime(raw_data["location"]["localtime"].split()[0], "%Y-%m-%d").strftime("%d.%m.%Y")
    weather = raw_data["current"]["condition"]["text"]
    temperature = raw_data["current"]["temp_c"]
    temperature_feel = raw_data["current"]["feelslike_c"]

    result = {
        "📅 День": day,
        "⛅️ Погода": weather,
        "🌡 Температура °C": temperature,
        "🖐 Температура по ощущению °C": temperature_feel
    }

    return result
