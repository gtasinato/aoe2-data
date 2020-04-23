from django.urls import path, include

from . import views

app_name = 'landing'
urlpatterns = [
    path('', views.index, name='index'),
    path('harvester/', include('harvester.urls') )
]
