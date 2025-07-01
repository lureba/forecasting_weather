from functionss.api_weather import call_api,formating
import psycopg2 as pg
import requests
import os


dbname = os.getenv("DBNAME")
user = os.getenv("USER_POSTGRES")
password = os.getenv("PASSWORD")
conn = pg.connect("user={} password={} dbname={}",user,password,dbname)
curs = conn.cursor()
api_key = os.getenv("API_WEATHER_KEY")


city_name = ["Guaratingueta","São José dos Campos","Lorena","Aparecida","Potim","Piquete","Cruzeiro","Cachoeira","Pindamonhangaba","Taubaté"]
url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
for i in city_name:
    data = formating(call_api(api_key=api_key,city_name=i))
    city_name = data['city_name']
    longitude = data['longitude']
    latitude = data['latitude']
    curs.execute("INSERT INTO coordinates values(%s,%s,%s)",(city_name,longitude,latitude))
    conn.commit()

curs.close()
conn.close()