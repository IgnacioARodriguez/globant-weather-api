from datetime import datetime

import beaufort_scale
import requests
import requests_cache
from decouple import config

from .exceptions.city_or_country_error import CityOrCountryError
from .exceptions.temperature_convertion_error import TemperatureError
from .exceptions.time_convertion_error import TimeConvertionError
from .exceptions.wind_degree_error import WindDegreeError


class WeatherApiServices(object):
    def __init__(self, city, country):
        requests_cache.install_cache('weather_api_cache', expire_after=120)
        self.weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={config("WEATHER_API_KEY")}'
        self.forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={config("WEATHER_API_KEY")}'
        self.weather = requests.get(self.weather_url).json()
        self.forecast = requests.get(self.forecast_url).json()

    def get_temperature_in_celsius(self, temperature):
        try:
            temperature_in_celsius = int(
                temperature) - 273.15
            return round(temperature_in_celsius, 2)
        except:
            raise TemperatureError

    def get_temperature_in_fahrenheit(self, temperature):
        try:
            temperature_in_fahrenheit = int(
                temperature) * 9/5 - 459.67
            return round(temperature_in_fahrenheit, 2)
        except:
            raise TemperatureError

    def degrees_to_compass(self, degrees):
        try:
            deg = int((degrees/22.5)+.5)
            compass = ["north", "north-north-east", "north-east", "east-north-east", "east", "east-south-east", "south-east", "south-south-east",
                       "south", "south-south-west", "south-west", "west-south-west", "west", "west-north-west", "north-west", "north-north-west"]
            return compass[(deg % 16)]
        except:
            raise WindDegreeError

    def utc_time_convertion(self, time):
        try:
            utc_time = datetime.fromtimestamp(time)
            return utc_time.strftime('%H:%M')
        except:
            raise TimeConvertionError

    def get_forecast_weather_data(self):
        if self.forecast['cod'] == '200':
            forecast_list = self.forecast['list']
            forecast_data = []
            for weather in forecast_list:
                forecast_data.append({
                    'temperature': f"{self.get_temperature_in_celsius(weather['main']['temp'])} °C, {self.get_temperature_in_fahrenheit(weather['main']['temp'])} °F",
                    'wind': f"{beaufort_scale.beaufort_scale_ms(self.weather['wind']['speed'], language='en')}, {self.weather['wind']['speed']} m/s, {self.degrees_to_compass(self.weather['wind']['deg'])}",
                    'cloudiness': weather['weather'][0]['description'],
                    'humidity': f"{weather['main']['humidity']}%",
                    'time': weather['dt_txt'],
                })
            return forecast_data
        else:
            raise CityOrCountryError

    def get_current_weather_data(self):
        if self.weather['cod'] == 200:
            weather_data = {
                'location_name': f"{self.weather['name']}, {self.weather['sys']['country']}",
                'temperature': f"{self.get_temperature_in_celsius(self.weather['main']['temp'])} °C, {self.get_temperature_in_fahrenheit(self.weather['main']['temp'])} °F",
                'wind': f"{beaufort_scale.beaufort_scale_ms(self.weather['wind']['speed'], language='en')}, {self.weather['wind']['speed']} m/s, {self.degrees_to_compass(self.weather['wind']['deg'])}",
                'cloudiness': self.weather['weather'][0]['description'],
                'pressure': f"{self.weather['main']['pressure']} hPa",
                'humidity': f"{self.weather['main']['humidity']}%",
                'sunrise': f"{self.utc_time_convertion(self.weather['sys']['sunrise'])}",
                'sunset': f"{self.utc_time_convertion(self.weather['sys']['sunset'])}",
                'geo_coordinates': f"[{self.weather['coord']['lat']}, {self.weather['coord']['lon']}]",
                'requested_time': f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                'forecast': self.get_forecast_weather_data(),
            }
            return weather_data
        else:
            raise CityOrCountryError
