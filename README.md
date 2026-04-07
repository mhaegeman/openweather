# OpenWeather Collector

![CI](https://github.com/mhaegeman/openweather/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Automated weather data pipeline — fetches live atmospheric data for configurable cities via the [OpenWeather API](https://openweathermap.org/api) and persists hourly snapshots to MySQL.

---

## What data does it collect?

For each city, the pipeline records three atmospheric measurements every 6 hours:

| Field | Unit | Description |
|---|---|---|
| `temperature` | Kelvin (K) | Ambient air temperature — 288 K ≈ 15 °C |
| `humidity` | % | Relative humidity |
| `pressure` | hPa | Atmospheric pressure at sea level |

Each run saves a snapshot table named `OpenWeather_YYYY_MM_DD_HH`, giving you a timestamped record of conditions across all tracked cities.

---

## Output

**Queried via Python:**

![Terminal output showing weather data for Dongen, Tilburg and Eindhoven](img/3.png)

**Queried via MySQL Workbench:**

![MySQL Workbench showing the OpenWeather snapshot table](img/3_1.png)

---

## Use cases

- **Trend analysis** — compare temperature and humidity across cities over time
- **Data engineering practice** — end-to-end pipeline: API → transform → SQL
- **Alerting baseline** — feed the snapshots into a dashboard or anomaly detector
- **Extend to more cities** — just add city names to the `CITIES` env var

---

## Architecture

```
OpenWeather API
      │  (REST, every 6h via cron)
      ▼
 collector.py  ──→  db.py  ──→  MySQL (Google Cloud SQL)
      │
  config.py (env vars: API key, DB URL, city list)
```

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

| Variable | Example | Description |
|---|---|---|
| `DB_URL` | `mysql+pymysql://user:pass@host/OpenWeather` | SQLAlchemy connection string |
| `OPENWEATHER_API_KEY` | `abc123...` | Free key from [openweathermap.org](https://openweathermap.org/api) |
| `CITIES` | `Dongen,Tilburg,Eindhoven` | Comma-separated list of cities |

### 3. Initialise the database schema

```python
from openweather.db import get_engine, init_schema
from openweather.config import DB_URL

init_schema(get_engine(DB_URL))
```

### 4. Run a collection

```bash
python -m openweather.collector
```

---

## Automation (cron)

Install the provided schedule to collect data 4× per day (midnight, 6h, 12h, 18h):

```bash
crontab crontab.txt
```

---

## Project Structure

```
openweather/
├── src/openweather/
│   ├── config.py         # env-var configuration
│   ├── db.py             # engine creation & persistence
│   └── collector.py      # API fetching & entry point
├── tests/
│   ├── test_collector.py
│   └── test_db.py
├── .github/workflows/
│   └── ci.yml            # lint + test on every push
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
