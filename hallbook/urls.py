"""hallbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from AoRole.serializers import JWTAuthentication
from AoRole.views import AllHallsAvailable, Ao_Pending, Ao_Report, AoApproval, Book_Hall, Contact_issue, Halls, Hallsdropdown, Hod_accepted_rejected, Hod_pending_forms, HodApproval, Logout, No_Response_Ao, Panel, Register, ResolveIssue, Userdetails
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(serializer_class=JWTAuthentication)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hall/', include('AoRole.urls')),
    path('user', Userdetails.as_view()),
    path('Halls', Halls.as_view()),
    path('logout', Logout.as_view()),
    path('LeftPanel', Panel.as_view()),
    path('bookhall', Book_Hall.as_view()),
    path('register', Register.as_view()),
    path('allhalls', AllHallsAvailable.as_view()),
    path('halls/dropdown', Hallsdropdown.as_view()),
    path('hod/pending', Hod_pending_forms.as_view()),
    path('hod/pending/<int:pk>', Hod_accepted_rejected.as_view()),
    path('HodApproval/<int:pk>', HodApproval.as_view()),
    path('Ao/Report/<int:pk>', Ao_Report.as_view()),
    path('Ao/pending', Ao_Pending.as_view()),
    path('Ao/approval/<int:pk>', AoApproval.as_view()),
    path('contact', Contact_issue.as_view()),
    path('contact/<int:pk>', ResolveIssue.as_view()),
    path('Ao/pending/status', No_Response_Ao.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
