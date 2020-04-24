from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'harvester'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:leaderboard_id>/', views.loading, name='loading'),
    path('archive/', views.archive, name='archive')
    # path('<str:games>/<int:leaderboard_id>/',  views.results, name='results')
]
