from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, RegisterUserForm


class UserLogin(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization',
                     'page_title': 'Login'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Registration', 'page_title': 'Sign in'}
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Logins user after successful registration
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
