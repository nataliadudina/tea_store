from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
      Custom User model that extends Django's built-in AbstractUser model.

      This model adds additional fields like email, activation_token, avatar, phone, and country.
      It also changes the default username field to an email field.
      """
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=50, blank=True, null=True, default='ghost', verbose_name="Username")
    activation_token = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.ImageField(upload_to="images/users/", blank=True, null=True, verbose_name="Image")
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Phone number")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Country")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
