from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserLogin, RegisterUser

app_name = 'users'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    ]
