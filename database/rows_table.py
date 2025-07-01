import psycopg2 as pg
import time
from functionss.api_weather import formating,call_api
import os
dbname = os.getenv("DBNAME")
host = os.getenv("HOST")
user = os.getenv("USER_POSTGRES")
password = os.getenv("PASSWORD")
conn = pg.connect("host={} dbname={} user={} password={}".format(host,dbname,user,password))
curs = conn.cursor()
api_key = os.getenv("API_WEATHER_KEY")
vale = ["Guaratingueta","São José dos Campos","Lorena","Aparecida","Potim","Piquete","Cruzeiro","Cachoeira","Pindamonhangaba","Taubaté"]

for city_name in vale:
    data = formating(call_api(api_key=api_key,city_name=city_name))
    curs.execute("INSERT INTO weather_ VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data["city_name"],data["main"],data["actual_temp"],data["feels_like"],data["temp_min"],data["temp_max"],data["actual_date"],data["humidity"],data["pressure"],data["sunset"],data["sunrise"]))
    conn.commit()
    print(f'ROW INSERT!\n VALUES: city_name:{data["city_name"]} main:{data["main"]} actual_temp:{data["actual_temp"]} feels_like:{data["feels_like"]} temp_min:{data["temp_min"]} temp_max:{data["temp_max"]} actual_date:{data["actual_date"]} sunset:{data["sunset"]} sunrise:{data["sunset"]}')
    time.sleep(1)

print("SUCESS OPERATION!")





