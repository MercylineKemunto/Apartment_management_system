from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates a tenant user and adds them to the Tenant group'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            with transaction.atomic():
                # Create or get the Tenant group
                tenant_group, created = Group.objects.get_or_create(name='Tenant')
                if created:
                    self.stdout.write(self.style.SUCCESS('Created Tenant group'))

                # Create the user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.groups.add(tenant_group)
                self.stdout.write(self.style.SUCCESS(f'Successfully created tenant user: {username}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating tenant user: {str(e)}')) 