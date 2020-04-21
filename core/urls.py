from django.urls import path

from . import views

urlpatterns = [
    path('summoner/update/<str:region>/<str:summoner_name>/', views.update_summoner, name='update_summoner'),
    path('summoner/<str:region>/<str:summoner_name>/', views.summoner, name='summoner'),
    path('', views.index, name='index'),
]