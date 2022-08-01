import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

from weather_api.services import WeatherApiServices

# Create your views here.


@api_view(['GET'])
def get_weather(request):
    weather = WeatherApiServices(request)
    print(weather)
    weather_json = weather.parsed_weather()
    return Response(weather_json)
