from urllib import request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from AoRole.models import Conference_Hall, Conference_Images

class JWTAuthentication(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        user_obj = User.objects.filter(email=attrs.get("username"))
        if user_obj:
            credentials['username'] = user_obj[0].username

        return super().validate(credentials)


class Conference_HallSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Conference_Hall
        exclude=['occupied']
        extra_kwargs = {'Description': {'required': False}}



class Conference_ImagesSerializer(serializers.ModelSerializer):
    hall=Conference_HallSerializer(read_only=True, many=True)

    class Meta:
        model=Conference_Images
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=('id', 'username', 'first_name', 'last_name', 'email')
