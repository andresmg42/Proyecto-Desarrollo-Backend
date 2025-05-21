import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

load_dotenv()

class Command(BaseCommand):
    help = 'Crea un usuario administrador por defecto usando variables de entorno'

    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario admin "{username}" creado'))
        else:
            self.stdout.write(self.style.WARNING(f'El usuario admin "{username}" ya existe'))