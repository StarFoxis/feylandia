from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.mainView.as_view()), name='game'),
    path('catalog/', views.catalogView.as_view(), name='catalog'),
    path('maze/', views.mazeGameView.as_view(), name='maze'),
]