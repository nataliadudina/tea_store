from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from .views import LoginUser, RegisterUser, ProfileUser, UserPasswordChange, activation_sent_view, activate_account, \
    CustomPasswordResetView

app_name = 'users'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # for changing password
    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
         name='password_change_done'),

    # for generating temporary password when reset
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('activation-sent/', activation_sent_view, name='activation_sent'),
    path('activate/<str:activation_token>/', activate_account, name='activate'),
    path('profile/', ProfileUser.as_view(), name='profile'),
]
