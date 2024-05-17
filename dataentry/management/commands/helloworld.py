from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints Hello World"

    def handle(self, *args, **kwargs):
        # logic
        self.stdout.write('Hello World')