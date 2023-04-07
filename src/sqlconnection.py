import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://maxime:1234@34.175.135.239')

engine.execute(sqlalchemy.schema.CreateSchema('OpenWeather'))