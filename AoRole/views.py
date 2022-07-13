from rest_framework import generics
from AoRole.models import Conference_Images
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
# from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from AoRole.serializers import Conference_HallSerializer, Conference_ImagesSerializer, UserSerializer
from .user import IsSuperUser

# Create your views here.

class Halls(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request):
        serializer=Conference_HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return serializer.errors
        
        Hall=serializer.data['id']
        files=request.FILES.getlist('image')
        for f in files:
            serializer=Conference_ImagesSerializer(data={'Hall':Hall,'image':f})
            if serializer.is_valid():
                serializer.save()
            else:
                return serializer.errors
        return Response({'message':'Uploaded succesfully'}, status=status.HTTP_201_CREATED)


class hallimage(generics.ListAPIView):
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        hall=self.kwargs.get('hall')
        return Conference_Images.objects.filter(Hall=hall)

    def get_serializer_class(self):
        return Conference_ImagesSerializer


class Userdetails(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        user=self.request.user.id
        return User.objects.filter(id=user)

    def get_serializer_class(self):
        return UserSerializer


class Logout(APIView):
    
    def post(self, request):
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()
        return Response({"message":"Successful Logout"}, status=status.HTTP_200_OK)