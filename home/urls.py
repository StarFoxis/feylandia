from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeView.as_view(), name='home'),
    path('info/', views.GameInfoView.as_view(), name='game-info'),
]