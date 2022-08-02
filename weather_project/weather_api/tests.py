from django.test import TestCase

from .services import WeatherApiServices

# Create your tests here.


class WeatherApiServicesTest(TestCase):
    def setUp(self):
        self.weather = WeatherApiServices('London', 'UK')

    def test_get_temperature_in_celsius(self):
        self.assertEqual(
            self.weather.get_temperature_in_celsius(293.15), 19.85)

    def test_get_temperature_in_fahrenheit(self):
        self.assertEqual(
            self.weather.get_temperature_in_fahrenheit(293.15), 67.73)

    def test_degrees_to_compass(self):
        self.assertEqual(self.weather.degrees_to_compass(230), 'south-west')

    def test_utc_time_convertion(self):
        self.assertEqual(
            self.weather.utc_time_convertion(1659327836), '04:23')

    def test_get_forecast_weather_data(self):
        self.assertEqual(
            self.weather.get_current_weather_data()['location_name'], 'London, GB')

    def test_get_current_weather_data(self):
        self.assertEqual(
            self.weather.get_current_weather_data()['location_name'], 'London, GB')
