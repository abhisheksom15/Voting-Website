from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        #if not User.objects.filter(username="admin").exists():
        #    User.objects.create_superuser("8979180488", "abhishek00159@gmail.com", "rds_kranti_vahini")
        #    self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
        print("working admin")
