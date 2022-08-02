from rest_framework.exceptions import APIException


class WindDegreeError(APIException):
    status_code = 502
    default_detail = "Wind degree is not valid"
    default_code = "WIND_DEGREE_ERROR"
