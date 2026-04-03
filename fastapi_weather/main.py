from fastapi import FastAPI
from .router import router as weather_router


app = FastAPI(title="Weather project")

app.include_router(weather_router)
