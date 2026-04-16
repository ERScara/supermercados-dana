from django.urls import path
from . import views

urlpatterns = [
    path('', views.acerca_de, name='acerca_de')
]