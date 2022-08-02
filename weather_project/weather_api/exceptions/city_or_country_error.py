from rest_framework.exceptions import APIException


class CityOrCountryError(APIException):
    status_code = 404
    default_detail = "City or country not found"
    default_code = "CITY_OR_COUNTRY_ERROR"
