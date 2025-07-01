import requests
import json
from datetime import datetime
def from_k_to_celsius(value):
    return round(value - 273.15,2)

def call_api(api_key,city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    data = requests.get(url=url).json()
    return data

def formating(data):
    actual_date = datetime.replace(datetime.now(),microsecond=0)
    weather_data = {
    "city_name":data["name"],
    "main":data["weather"][0]["main"],
    "actual_temp":from_k_to_celsius(data["main"]["temp"]),
    "feels_like":from_k_to_celsius(data["main"]["feels_like"]),
    "temp_min":from_k_to_celsius(data["main"]["temp_min"]),
    "temp_max":from_k_to_celsius(data["main"]["temp_max"]),
    "actual_date":actual_date,
    "humidity":data["main"]["humidity"],
    "pressure":data["main"]["pressure"],
    "sunset": datetime.fromtimestamp(data["sys"]["sunset"]),
    "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
    "longitude": data["coord"]["lon"],
    "latitude": data["coord"]["lat"]
    }
    return weather_data