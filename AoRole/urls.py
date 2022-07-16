from django.urls import path
from . import views

urlpatterns = [
    path('Halls', views.Halls.as_view()),
    path('<int:hall>', views.hallimage.as_view())
]
