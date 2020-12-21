from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import SignUpForm
from .models import *

def deactivate_person(user):
    for person in PersonModel.objects.filter(user=user):
        person.active = False
        person.save()

def require_skins(request):
    skins = SkinModel.objects.filter(style_id=request.GET.get('style_id')).values('id', 'name', 'image')
    data = {'skins': list(skins)}

    return JsonResponse(data)

def select_person(request):
    deactivate_person(request.user)

    person = PersonModel.objects.get(id=request.GET.get('person_id'), user=request.user)
    person.active = True
    person.save()

    data = {'persons': list(PersonModel.objects.filter(user=request.user).values('id', 'active'))}
    return JsonResponse(data)


class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = 'home'

class ProfileView(generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *argv, **kwargs):
        context = super().get_context_data(*argv, **kwargs)
        context['persons'] = PersonModel.objects.filter(user=self.request.user)
        return context

class CreatePersonView(generic.CreateView):
    template_name = 'create_person.html'
    fields = []

    def post(self, request, *argv, **kwargs):
        user = request.user
        style = StyleModel.objects.get(id=request.POST.get('style_id'))
        skin = SkinModel.objects.get(id=request.POST.get('skin_id'))
        deactivate_person(user)
        person = PersonModel.objects.create(user=user, style=style, skin=skin, active=True)
        person.save()
        # print('~'*100, person, user, skin, person, '~'*100, sep='\n')

        return redirect(request.path)

    def get_context_data(self, *argv, **kwargs):
        context = super().get_context_data(*argv, **kwargs)
        context['styles'] = StyleModel.objects.all()
        return context

    def get_queryset(self, *argv, **kwargs):
        style = StyleModel.objects.all()
        return style

class DeletePersonView(generic.DeleteView):
    model = PersonModel
    context_object_name = 'person'
    template_name = 'delete_person.html'
    success_url = reverse_lazy('profile')

    def post(self, request, *argv, **kwargs):
        response = super().post(request, *argv, **kwargs)
        person_active = PersonModel.objects.filter(user=request.user)
        if person_active and not person_active.filter(active=True):
            person = PersonModel.objects.filter(user=request.user)[0]
            person.active = True
            person.save()
        return response

    def get_context_data(self, *argv, **kwargs):
        context = super().get_context_data(*argv, **kwargs)
        # context['person'] = 
        return context

class PersonDetailView(generic.DetailView):
    model = PersonModel
    context_object_name = 'person'
    template_name = 'person-detail.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(
            *args, **kwargs
        ).filter(user=self.request.user)

    def get_context_data(self, *argv, **kwargs):
        context = super().get_context_data(*argv, **kwargs)
        # context['person'] = self.object
        context['skills'] = context['person'].style.skill.all()
        return context