"""Unit tests for the db module."""
from unittest.mock import MagicMock, patch

import pandas as pd

from openweather.db import get_engine, save_weather


class TestGetEngine:
    def test_returns_engine(self):
        with patch("openweather.db.sqlalchemy.create_engine") as mock_create:
            mock_create.return_value = MagicMock()
            engine = get_engine("mysql+pymysql://user:pass@host/db")

        mock_create.assert_called_once_with("mysql+pymysql://user:pass@host/db")
        assert engine is mock_create.return_value


class TestSaveWeather:
    def test_calls_to_sql(self):
        df = pd.DataFrame({"city": ["Tilburg"], "temperature": [289.5], "humidity": [78], "pressure": [1012]})
        mock_engine = MagicMock()

        with patch.object(df.__class__, "to_sql") as mock_to_sql:
            save_weather(df, mock_engine, "OpenWeather_2024_01_01_12")

        mock_to_sql.assert_called_once_with(
            "OpenWeather_2024_01_01_12",
            mock_engine,
            if_exists="replace",
            index=False,
        )
