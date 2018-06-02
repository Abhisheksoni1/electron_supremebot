from django.core.management import BaseCommand
from supreme_captcha_harvester import run_harvester


class Command(BaseCommand):
    help = 'start captcha server to bypass it'

    def handle(self, *args, **options):
        run_harvester.main()