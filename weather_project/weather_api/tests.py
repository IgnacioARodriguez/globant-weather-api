from django.test import TestCase
import unittest

from weather_project.weather_api.services import WeatherApiServices

# Create your tests here.


class WeatherApiServicesTest(TestCase):
    def setUp(self):
        self.weather = WeatherApiServices()

    def test_get_weather(self):
        self.assertEqual(self.weather.get_weather(), 'Hello World')
