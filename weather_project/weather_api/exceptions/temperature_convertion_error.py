from rest_framework.exceptions import APIException


class TemperatureError(APIException):
    status_code = 502
    default_detail = "Temperature is not valid"
    default_code = "TEMPERATURE_ERROR"
