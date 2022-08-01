import requests
import requests_cache
import beaufort_scale
from decouple import config
from datetime import datetime


class WeatherApiServices(object):
    def __init__(self, request):
        requests_cache.install_cache('weather_api_cache', expire_after=120)
        self.city = request.query_params['city']
        self.country = request.query_params['country']
        self.weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&appid={config("WEATHER_API_KEY")}'
        self.forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={self.city},{self.country}&appid={config("WEATHER_API_KEY")}'
        self.weather = requests.get(self.weather_url).json()
        self.forecast = requests.get(self.forecast_url).json()

    def get_temperature_in_celsius(self, temperature):
        temperature_in_celsius = int(
            temperature) - 273.15
        return round(temperature_in_celsius, 2)

    def get_temperature_in_fahrenheit(self, temperature):
        temperature_in_fahrenheit = int(
            temperature) * 9/5 - 459.67
        return round(temperature_in_fahrenheit, 2)

    def degrees_to_compass(self, degrees):
        deg = int((degrees/22.5)+.5)
        compass = config('COMPASS_DIRECTION')
        return compass[(deg % 16)]

    def utc_time_convertion(self, time):
        utc_time = datetime.fromtimestamp(time)
        return utc_time.strftime('%H:%M')

    def parsed_forecast(self):
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

    def parsed_weather(self):
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
            'forecast': self.parsed_forecast(),
        }
        return weather_data
