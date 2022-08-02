from rest_framework.decorators import api_view
from rest_framework.response import Response

from weather_api.services import WeatherApiServices

# Create your views here.


@api_view(['GET'])
def get_weather(request):
    if request.query_params.get('city') is None or request.query_params.get('country') is None:
        return Response({'error': 'Please provide city and country'})
    else:
        city = request.query_params['city']
        country = request.query_params['country']
        try:
            weather_data = WeatherApiServices(
                city, country).get_current_weather_data()
            return Response(weather_data)
        except Exception as e:
            return Response(str(e))
