from django.shortcuts import render
from django.views import generic

class mainView(generic.TemplateView):
    template_name = 'game.html'

class catalogView(generic.TemplateView):
    template_name = 'catalog.html'

class mazeGameView(generic.TemplateView):
    template_name = 'maze.html'

