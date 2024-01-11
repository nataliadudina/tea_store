from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, \
    CustomPasswordResetForm
from users.models import User


class LoginUser(LoginView):
    """
       View for logging in users.

       It uses the LoginUserForm for validation and renders the 'users/login.html' template.
       After successful login, it redirects the user to the home page.
       """
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization',
                     'page_title': 'Login'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    """
       View for registering new users.

       It uses the RegisterUserForm for validation and renders the 'users/register.html' template.
       After successful registration, it sends an email to the user with an activation link.
       The user is then redirected to the activation sent page.
       """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Registration', 'page_title': 'Sign in'}
    success_url = reverse_lazy('users:activation_sent')  # for verifying

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.instance  # Gets user object from a form without saving

        # Builds the absolute URI for the activation link
        activation_url = self.request.build_absolute_uri(
            reverse_lazy('users:activate', args=[new_user.activation_token]))

        # Sends an email to the user with the activation link
        send_mail(
            subject='Welcome to TeaShop! Activate Your Account!',
            message=f'Thank you for registering! To activate your account, click on the following link:\n\n{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return response


class ProfileUser(LoginRequiredMixin, UpdateView):
    """
       View for updating user profiles.

       It uses the ProfileUserForm for validation and renders the 'users/profile.html' template.
       Only logged in users can access this view.
       After successful update, it redirects the user to the home page.
       """
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': 'Profile',
        'page_title': 'Profile',
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('home')

    def get_object(self, queryset=None):
        # Returns the current logged in user
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """
      View for changing the user's password.

      It uses the UserPasswordChangeForm for validation and renders the 'users/password_change_form.html' template.
      After successful password change, it redirects the user to the 'password_change_done' page.
      """
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': 'Change password', 'page_title': 'Change password'}


def activation_sent_view(request):
    """Function-based view for rendering the 'users/activation_sent.html' template."""
    return render(request, 'users/activation_sent.html')


def activate_account(request, activation_token):
    """
      Function to activate a user's account.

      It finds the user with the given activation token, marks the user as active,
      removes the activation token, logs the user in, and redirects the user to the profile page.
      """
    user = get_object_or_404(User, activation_token=activation_token)
    user.is_active = True
    user.activation_token = None
    user.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect(reverse_lazy('users:profile'))


class CustomPasswordResetView(PasswordResetView):
    """
     View for resetting the user's password.

     It uses the CustomPasswordResetForm for validation and renders the 'users/password_reset_form.html' template.
     After successful password reset, it redirects the user to the 'password_reset_done' page.
     """
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
