"""Database helpers: engine creation, schema init, and data persistence."""
import logging

import pandas as pd
import sqlalchemy
from sqlalchemy import text

logger = logging.getLogger(__name__)


def get_engine(db_url: str) -> sqlalchemy.Engine:
    return sqlalchemy.create_engine(db_url)


def init_schema(engine: sqlalchemy.Engine, schema: str = "OpenWeather") -> None:
    """Create the target schema if it does not already exist."""
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS `{schema}`"))
        conn.commit()
    logger.info("Schema '%s' ready.", schema)


def save_weather(df: pd.DataFrame, engine: sqlalchemy.Engine, table: str) -> None:
    """Write a DataFrame to *table*, replacing any existing data for that snapshot."""
    df.to_sql(table, engine, if_exists="replace", index=False)
    logger.info("Saved %d row(s) to table '%s'.", len(df), table)
