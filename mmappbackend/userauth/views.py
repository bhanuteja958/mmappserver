from .serializers import UserRegistrationSerializer, UserLoginSerializer,AuthUserSerializer
from rest_framework.views import APIView
from .utils import create_new_user
from global_utils import getAPIResponse
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class RegisterUser(APIView):
    def post (self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            new_user = create_new_user(serializer.data['username'],serializer.data["email"], serializer.data["password"])
            return Response(getAPIResponse(False, 'Successfully created user',data={
                "user_details": new_user
            }),status=status.HTTP_201_CREATED)
        else:
            return Response(getAPIResponse(True, 'Not valid data sent for creating customer'),status=status.HTTP_400_BAD_REQUEST)

class SignInUser(APIView):
    def post (self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            auth_user = authenticate(username=serializer.data['username'],password=serializer.data['password'])
            if auth_user is None:
                return Response(getAPIResponse(True, 'Invalid Username/Password. Please try again'), status=status.HTTP_400_BAD_REQUEST)
            else:
                login(request, user=auth_user)
                user_data = AuthUserSerializer(auth_user).data
                return Response(getAPIResponse(False,'Successfully logged in user',data={
                    "user_details": user_data
                }), status=status.HTTP_200_OK)
        else:
            return Response(getAPIResponse(True, 'Error while logging in user'), status.HTTP_400_BAD_REQUEST)


class SignOutUser(APIView):
    def post(self,request):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response(getAPIResponse(False, 'Successfully logged out'), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(getAPIResponse(True, 'Error While logging out user', errors=[str(e)]))


