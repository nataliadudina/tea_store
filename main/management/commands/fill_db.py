from django.core.management.base import BaseCommand
from django.core.management import call_command
from main.models import TeaProduct, TeaCategory


class Command(BaseCommand):
    help = 'Clears database and loads data from data.json fixture'

    def handle(self, *args, **options):
        # Deletes data from db
        TeaProduct.objects.all().delete()
        TeaCategory.objects.all().delete()

        # Loads data from fixture
        call_command('loaddata', 'data.json')
