import json
from django.core.management.base import BaseCommand
from sticker.models import Countries

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open("countries.json") as f:
            countries = json.load(f)

        for country in countries:
            name = country["name"]
            code = country["code"]
            Countries.objects.create(name=name, code=code)
        self.stdout.write(self.style.SUCCESS("Countries loaded successfully."))