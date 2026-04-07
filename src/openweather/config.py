"""Configuration loaded from environment variables."""
import os

from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Required environment variable '{key}' is not set.")
    return value


# Database
DB_URL: str = _require("DB_URL")

# OpenWeather API
API_KEY: str = _require("OPENWEATHER_API_KEY")

# Comma-separated list of cities to track
CITIES: list[str] = [
    c.strip()
    for c in os.getenv("CITIES", "Dongen,Tilburg,Eindhoven").split(",")
    if c.strip()
]
