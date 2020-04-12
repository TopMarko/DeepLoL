from django.urls import path

from . import views

urlpatterns = [
    path('summoner/<str:region>/<str:summoner_name>/', views.summoner, name='summoner'),
]