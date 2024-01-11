from django.core.management.base import BaseCommand
from django.core.management import call_command
from main.models import TeaProduct, TeaCategory

"""
This is a custom Django management command that clears the database and loads new data from a JSON fixture file.

Before running this command, it's recommended to run the `dumpdata` command first 
to create a backup of the current database state. This can be done with the following command:
           python manage.py dumpdata <app_name> > data.json

Then, you can clear the database and load new data with this command:
           python manage.py fill_db

Please note that this command will permanently delete all data from the `TeaProduct` and `TeaCategory` tables. 
Be sure to backup your data before running this command.
"""


class Command(BaseCommand):
    help = 'Clears database and loads data from data.json fixture'

    def handle(self, *args, **options):
        # Deletes data from db
        TeaProduct.objects.all().delete()
        TeaCategory.objects.all().delete()

        # Loads data from fixture
        call_command('loaddata', 'data.json')
