from django.shortcuts import render
from django.views import generic

from registration.models import *

class homeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *argv, **kwargs):
        context = super().get_context_data(*argv, **kwargs)

        if self.request.user.is_authenticated:
            context['is_persons'] = bool(PersonModel.objects.filter(user=self.request.user, active=True))
        return context

class GameInfoView(generic.TemplateView):
    template_name = 'game_info.html'