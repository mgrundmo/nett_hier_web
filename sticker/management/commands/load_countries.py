import json
from django.core.management.base import BaseCommand
from sticker.models import Countries

class Command(BaseCommand):
    #used to import countries from json list
    def handle(self, *args, **kwargs):
        with open("countries.json") as file:
            countries = json.load(file)

        for country in countries:
            name = country["name"]
            code = country["code"]
            Countries.objects.create(name=name, code=code)
        self.stdout.write(self.style.SUCCESS("Countries loaded successfully."))