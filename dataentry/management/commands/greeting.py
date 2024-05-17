from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Greetings loser"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Specifies user name')

    def handle(self, *args, **kwargs):
        # logic
        name = kwargs['name']
        greeding = f'Hi {name}, Good Morning'
        self.stdout.write(self.style.SUCCESS(greeding))