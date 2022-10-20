import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine('mysql+pymysql://maxime:1234@34.175.135.239/OpenWeather')

#engine.execute(sqlalchemy.schema.CreateSchema('OpenWeather'))

df = pd.read_sql('SELECT * FROM OpenWeather_2022_10_20_12', engine)
print('OpenWeather_2022_10_20_12 table')
print(df)