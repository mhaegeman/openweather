# OpenWeather Collector

![CI](https://github.com/mhaegeman/openweather/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Automated weather data pipeline — fetches temperature, humidity, and pressure for configurable cities via the [OpenWeather API](https://openweathermap.org/api) and persists hourly snapshots to MySQL.

---

## Architecture

```
OpenWeather API
      │
      ▼
 collector.py   ──→   db.py   ──→   MySQL (Google Cloud SQL)
      │
  config.py (env vars)
```

Data is collected 4× per day via cron and stored in timestamped tables (`OpenWeather_YYYY_MM_DD_HH`).

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set DB_URL, OPENWEATHER_API_KEY, and optionally CITIES
```

### 3. Initialise the database schema

```python
from openweather.db import get_engine, init_schema
from openweather.config import DB_URL

init_schema(get_engine(DB_URL))
```

### 4. Run a collection

```bash
PYTHONPATH=src python -m openweather.collector
```

---

## Automation (cron)

Install the provided schedule to collect data 4× per day:

```bash
crontab crontab.txt
```

Schedule: `0 0,6,12,18 * * *`

---

## Project Structure

```
openweather/
├── src/openweather/
│   ├── config.py       # env-var configuration
│   ├── db.py           # engine creation & persistence
│   └── collector.py    # API fetching & entry point
├── tests/
│   ├── test_collector.py
│   └── test_db.py
├── .github/workflows/
│   └── ci.yml          # lint + test on every push
├── .env.example
├── crontab.txt
├── requirements.txt
└── requirements-dev.txt
```

---

## Development

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src
```

The CI pipeline runs `ruff` (linting) and `pytest` (tests) on every push.
