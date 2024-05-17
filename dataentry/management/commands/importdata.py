from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError


class Command(BaseCommand):
    help = "Import data from CSV files"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        model = None

        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name) 
                break
            except LookupError:
                continue
        if not model:
            raise CommandError(f'Model "{model_name}" does not exist')
            
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            if csv_header != model_fields:
                raise DataError(f'CSV file does not match with {model_name} table fields')
            for row in reader:
                model.objects.create(**row)
            


        self.stdout.write(self.style.SUCCESS('Dataset imported successfully'))