from django.urls import path

from . import views

app_name = 'harvester'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/',  views.result, name='result')
]
