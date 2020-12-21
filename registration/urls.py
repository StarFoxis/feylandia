from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('create_person/', login_required(views.CreatePersonView.as_view()), name='create-person'),
    path('delete_person/<int:pk>/delete/', login_required(views.DeletePersonView.as_view()), name='delete-person'),
    path('person-detail/<int:pk>/', login_required(views.PersonDetailView.as_view()), name='person-detail'),

    path('ajax/require_skins/', login_required(views.require_skins), name='require-skins'),
    path('ajax/select_person/', login_required(views.select_person), name='select-person'),
]