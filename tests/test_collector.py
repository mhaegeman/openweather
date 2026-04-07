"""Unit tests for the collector module."""
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import requests

from openweather.collector import collect, fetch_weather


FAKE_API_KEY = "test_key"
FAKE_RESPONSE = {
    "main": {
        "temp": 289.5,
        "humidity": 78,
        "pressure": 1012,
    }
}


def _mock_get(json_data: dict, status_code: int = 200):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    if status_code >= 400:
        mock.raise_for_status.side_effect = requests.HTTPError(response=mock)
    else:
        mock.raise_for_status.return_value = None
    return mock


class TestFetchWeather:
    def test_returns_correct_fields(self):
        with patch("openweather.collector.requests.get", return_value=_mock_get(FAKE_RESPONSE)):
            result = fetch_weather("Tilburg", FAKE_API_KEY)

        assert result["city"] == "Tilburg"
        assert result["temperature"] == 289.5
        assert result["humidity"] == 78
        assert result["pressure"] == 1012

    def test_passes_correct_params(self):
        with patch("openweather.collector.requests.get", return_value=_mock_get(FAKE_RESPONSE)) as mock_get:
            fetch_weather("Dongen", FAKE_API_KEY)

        mock_get.assert_called_once_with(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"appid": FAKE_API_KEY, "q": "Dongen"},
            timeout=10,
        )

    def test_raises_on_http_error(self):
        with patch("openweather.collector.requests.get", return_value=_mock_get({}, 404)):
            with pytest.raises(requests.HTTPError):
                fetch_weather("UnknownCity", FAKE_API_KEY)


class TestCollect:
    def test_collects_all_cities(self):
        with patch("openweather.collector.requests.get", return_value=_mock_get(FAKE_RESPONSE)):
            df = collect(["Dongen", "Tilburg", "Eindhoven"], FAKE_API_KEY)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert set(df["city"]) == {"Dongen", "Tilburg", "Eindhoven"}

    def test_skips_failed_city(self):
        responses = [
            _mock_get(FAKE_RESPONSE),
            _mock_get({}, 500),
            _mock_get(FAKE_RESPONSE),
        ]
        with patch("openweather.collector.requests.get", side_effect=responses):
            df = collect(["Dongen", "BAD_CITY", "Eindhoven"], FAKE_API_KEY)

        assert len(df) == 2
        assert "BAD_CITY" not in df["city"].values

    def test_returns_empty_dataframe_when_all_fail(self):
        with patch("openweather.collector.requests.get", side_effect=requests.ConnectionError):
            df = collect(["X", "Y"], FAKE_API_KEY)

        assert df.empty
