from django.contrib.auth.models import User
from rest_framework import authentication

class AllowAll(authentication.BaseAuthentication):
    def authenticate(self, request):
        return (User.objects.get(id=1), None)