from rest_framework import generics
from AoRole.models import Conference_Hall, Conference_Images
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
        print(request.data)
        serializer=Conference_HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return Response(serializer.errors)
        
        Hall=serializer.data['id']
        files=request.FILES.getlist('image')
        for f in files:
            serializerimage=Conference_ImagesSerializer(data={'Hall':Hall,'image':f})
            if serializerimage.is_valid():
                serializerimage.save()
            else:
                return Response(serializerimage.errors)
        return Response(serializer.data)
    
    def get(self, request):
        halls=Conference_Hall.objects.filter(occupied=False)
        serializer=Conference_HallSerializer(halls, many=True)
        return Response(serializer.data)

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