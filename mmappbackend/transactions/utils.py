from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

NOT_AUTHENTICATED_RESPOSNE = {
    "error": True, 
    "message": 'Invalid Username/Password'
}

def custom_exception_handler(exc, context):
    if exc.get_codes() == 'authentication_failed':
        return Response(NOT_AUTHENTICATED_RESPOSNE, status=status.HTTP_401_UNAUTHORIZED)
    return exception_handler(exc, context)