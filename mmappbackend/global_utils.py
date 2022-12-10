from rest_framework.views import exception_handler
from rest_framework.response import Response

def getAPIResponse(is_error, message, data=[],errors=[] ):
    return {
        "is_error": is_error,
        "message": message,
        "data": data,
        "error": errors
    }

def custom_exception_handler(exc, context):
    exc_response = exception_handler(exc, context)
    if exc_response is not None:
        status_code = exc_response.status_code
        errors=exc.detail 
    else: 
        status_code = 400
        errors = str(exc)
    return Response(
        getAPIResponse(True, 'Some error occured', errors=errors),
        status = status_code
    )