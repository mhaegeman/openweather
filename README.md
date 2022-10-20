# Open Weather Project

## 1. Create VM instance on Google Cloud Console

In the Compute Engine section a created a VM instance e2-micro named “test-weather”



## 2. Create and connect an SQL instance to the VM

In the SQL section I created an instance of a MySQL 8.0 database named “openweather-db”

In the SQL section I then created a new connection to get access to the database from the VM instance


That way, running the sqlconnection.py file I was able to connect to the DB and create a new schema called “OpenWeather” where I would save the data.

## 3. Get the OpenWeather data of Netherland cities and save it in the SQL instance

I created a free account in https://openweathermap.org to get a API key, then using the script datacollection.py, I was able to connect and extract the live weather info from cities in a list (in this example I did it for Dongen, Tilburg and Eindhoven but more could have been add to the list).

I extracted the temperature, humidity and pressure information for each city and then saved them in a table named “OpenWeather_”+date (with the date in the format "%Y_%m_%d_%H") to have a new table per date. 
Here is an example of the table create the 20/10/2022 at 12h (showed in the VM with the showdata.py script):


## 4. Automate this process with a cron job

In order to be able to repeat automatically this process every day, I created a crontab with those parameters (called crontab.txt in the repository):

It runs the python script datacollection.py 4 times a day (at 00h00, 6h00, 12h00 and 18h00) and it saves the output of the script in a logs.txt file that allows us to make sure the cron worked. 


With more time…
There are plenty of things we can do to save and display this weather data. First we can extend our weather zone to more cities in the area, it is possible with the API to give it a geolocation zone (giving coordinates) and getting the data of all cities in that zone.

Coding wise, with more time I would create a table per city, saving every new record as another row of that table. I would also include all the information features that OpenWeather has. 
