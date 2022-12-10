from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']

class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=300, required=True)
    password=serializers.CharField(max_length=300, required=True)
   

class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=['auth_token']
    
    def get_auth_token(self,obj):
        token = Token.objects.create(user=obj)
        return token.key