import sqlalchemy
import requests
import datetime
import pandas as pd

current_full_time = datetime.datetime.now()
current_time = current_full_time.strftime("%Y_%m_%d_%H")

engine = sqlalchemy.create_engine('mysql+pymysql://maxime:1234@34.175.135.239/OpenWeather')

API_key = "ENTER_YOUR_API_KEY"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

df=pd.DataFrame({'cities':["Dongen", "Tilburg", "Eindhoven"],
                 'temperature':[0,0,0],
                 'humidity':[0,0,0],
                 'pressure':[0,0,0]})

for city_name in df.cities.values:
    Final_url = base_url + "appid=" + API_key + "&q=" + city_name
    print(current_full_time, city_name)
    weather_data = requests.get(Final_url).json()

    df.loc[df.cities==city_name, 'temperature'] = weather_data['main']['temp']
    df.loc[df.cities==city_name, 'humidity'] = weather_data['main']['humidity']
    df.loc[df.cities==city_name, 'pressure'] = weather_data['main']['pressure']

df_name = 'OpenWeather_'+current_time
df.to_sql(df_name, engine, index=False)

#%%
