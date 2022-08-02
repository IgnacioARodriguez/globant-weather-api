from rest_framework.exceptions import APIException


class TimeConvertionError(APIException):
    status_code = 502
    default_detail = "Time is not valid"
    default_code = "TIME_CONVERTION_ERROR"
