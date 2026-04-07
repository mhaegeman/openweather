"""Unit tests for the db module."""
from unittest.mock import MagicMock, patch

import pandas as pd

from openweather.db import get_engine, init_schema, save_weather


class TestGetEngine:
    def test_returns_engine(self):
        with patch("openweather.db.sqlalchemy.create_engine") as mock_create:
            mock_create.return_value = MagicMock()
            engine = get_engine("mysql+pymysql://user:pass@host/db")

        mock_create.assert_called_once_with("mysql+pymysql://user:pass@host/db")
        assert engine is mock_create.return_value


class TestInitSchema:
    def test_connects_at_server_level(self):
        """init_schema must strip the database from the URL before connecting,
        otherwise MySQL rejects the connection when the schema does not yet exist."""
        mock_url = MagicMock()
        mock_url.set.return_value = mock_url

        mock_engine = MagicMock()
        mock_engine.url = mock_url

        mock_server_engine = MagicMock()
        mock_conn = MagicMock()
        mock_server_engine.connect.return_value.__enter__ = lambda s: mock_conn
        mock_server_engine.connect.return_value.__exit__ = MagicMock(return_value=False)

        with patch("openweather.db.sqlalchemy.create_engine", return_value=mock_server_engine):
            init_schema(mock_engine, schema="OpenWeather")

        # URL must have database stripped before creating the server engine
        mock_url.set.assert_called_once_with(database=None)
        mock_server_engine.dispose.assert_called_once()


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
