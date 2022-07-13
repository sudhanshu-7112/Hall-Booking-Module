from django.urls import path
from . import views

urlpatterns=[
    path('Halls',views.Halls.as_view()),
    path('images',views.Images.as_view()),
    path('logout',views.Logout.as_view()),
    path('hall/<int:hall>',views.hallimage.as_view())
]