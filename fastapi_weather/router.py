from fastapi import APIRouter
from .weather_logic import formatted_weather_data, get_weather_now_func

router = APIRouter()

@router.get("/weather")
def show_weather():
    raw_data = get_weather_now_func()
    weather_json = formatted_weather_data(raw_data=raw_data)

    return weather_json
