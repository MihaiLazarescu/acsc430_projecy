import csv
from django.core.management.base import BaseCommand
from django.apps import apps
import datetime

class Command(BaseCommand):
    help = 'Export data from database to a csv file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help= 'Model name to export')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass

        if not model:
            self.stderr.write(f'Could not find model {model_name}')
            return
        
        

        data = model.objects.all()

        timestamp = datetime.datetime.now().strftime("%Y-%d-%m-%H-%M-%S")
        

        file_path = f'exported_{model_name}_data_{timestamp}.csv'
        

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow([field.name for field in model._meta.fields])

            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfully'))