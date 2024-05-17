from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help = "Insert data into database"

    def handle(self, *args, **kwargs):
        # logic
        dataset = [
            {'roll_no':1,'name':'Mike', 'age':21},
            {'roll_no':2,'name':'John', 'age':25},
            {'roll_no':3,'name':'Antreas', 'age':20},
        ]

        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()

            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
                self.stdout.write(self.style.SUCCESS('Dataset inserted successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Student {roll_no} already exists'))

            
        