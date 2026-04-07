"""Fetch current weather for a list of cities and persist the snapshot to MySQL."""
import datetime
import logging

import pandas as pd
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str, api_key: str) -> dict:
    """Return temperature (K), humidity (%), and pressure (hPa) for *city*."""
    response = requests.get(BASE_URL, params={"appid": api_key, "q": city}, timeout=10)
    response.raise_for_status()
    main = response.json()["main"]
    return {
        "city": city,
        "temperature": main["temp"],
        "humidity": main["humidity"],
        "pressure": main["pressure"],
    }


def collect(cities: list[str], api_key: str) -> pd.DataFrame:
    """Fetch weather for all *cities*, skipping any that fail."""
    records = []
    for city in cities:
        try:
            records.append(fetch_weather(city, api_key))
            logger.info("Fetched data for %s.", city)
        except requests.RequestException as exc:
            logger.error("Could not fetch data for %s: %s", city, exc)
    return pd.DataFrame(records)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )

    # Import config here so tests can patch it without triggering env-var checks
    from openweather.config import API_KEY, CITIES, DB_URL  # noqa: PLC0415
    from openweather.db import get_engine, save_weather  # noqa: PLC0415

    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H")
    df = collect(CITIES, API_KEY)

    if df.empty:
        logger.warning("No data collected — nothing written to the database.")
        return

    engine = get_engine(DB_URL)
    save_weather(df, engine, f"OpenWeather_{timestamp}")


if __name__ == "__main__":
    main()
