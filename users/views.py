from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from django.views.generic import FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import (LoginRequiredMixin,)
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.defaults import page_not_found, server_error


from .models import User, Profile
from .forms import UserForm, ProfileForm, ProfileEditForm, LoginForm
from django.conf import settings


class Login(LoginView):
    template_name = 'user/login.html'

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)

        return context

    def get_login_success_url(self, form):
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        # Redirect staff members to dashboard as that's the most likely place
        # they'll want to visit if they're logging in.
        if self.request.user.is_staff:
            return reverse('/')

        return settings.LOGIN_REDIRECT_URL


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'user/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('/'))



# Edits the profile given the user
class EditUserProfileView(LoginRequiredMixin, UpdateView):  # Note that we are using UpdateView and not FormView
    model = Profile
    template_name = "user/profile.html"
    form_class = ProfileEditForm

    def get_success_url(self, *args, **kwargs):
        user = self.kwargs['pk']
        return reverse('user:user-profile', kwargs={'pk': user})

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        print("Usuario:::::, ", user)

        try:
            profile = Profile.objects.get(user_id=user)
        except ObjectDoesNotExist:
            u = '{}'.format(self.request.user).split('@')
            print("User Name: ", u[0])
            profile = Profile.objects.create(user_id=user.id, user_name=u[0], contacto='+258840000000',
                                             sexo=1, terms=1, data_nascimento="2000-01-01")
        print("Usuario a Editar: ", profile)

        # profile = Profile.objects.get(user_id=user)
        return profile


# User Profile View
class UserProfile(LoginRequiredMixin, DetailView):
    queryset = User
    template_name = './user/user_home.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        user = self.request.user
        user_id = user.id
        try:
            profile = Profile.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            profile = []
            print("Perfil para esse usuario nao existe")

        print("User em causa: ", user_id, "Perfil: ", profile)
        context['profile'] = profile
        context['user'] = user

        return context


def user_exists(user_name):
    try:
        Profile.objects.get(user_name=user_name)
    except ObjectDoesNotExist:
        return False

    return True


def get_user_id(email_or_user_name):
    q = User.objects.get(email=email_or_user_name)
    user_id = q.id
    return user_id


def handler404(request, exception, template_name="./internationaldonations/404.html"):
    return page_not_found(request, exception, template_name)


def handler500(request, template_name="./internationaldonations/500.html"):
    return server_error(request, template_name)

