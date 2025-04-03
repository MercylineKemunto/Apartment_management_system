from django.core.management.base import BaseCommand
from api.models import Unit, Apartment

class Command(BaseCommand):
    help = 'Creates a new unit in an apartment'

    def add_arguments(self, parser):
        parser.add_argument('apartment_name', type=str, help='Name of the apartment')
        parser.add_argument('unit_number', type=str, help='Unit number')
        parser.add_argument('size', type=float, help='Size in square meters')
        parser.add_argument('rent_amount', type=float, help='Monthly rent amount')

    def handle(self, *args, **options):
        try:
            apartment = Apartment.objects.get(name=options['apartment_name'])
            
            unit = Unit.objects.create(
                apartment=apartment,
                unit_number=options['unit_number'],
                size=options['size'],
                rent_amount=options['rent_amount'],
                is_occupied=False
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created unit {unit.unit_number} in {apartment.name}'
                )
            )
            
        except Apartment.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Apartment "{options["apartment_name"]}" does not exist'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating unit: {str(e)}')
            ) 