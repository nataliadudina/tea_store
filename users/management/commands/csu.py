import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('SUPERUSER_EMAIL'),
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
