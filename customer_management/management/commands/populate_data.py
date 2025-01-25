import random
from django.core.management import BaseCommand
from faker import Faker
from customer_management.models import Address, AppUser, CustomerRelationship

# @author Pradeep Juturu

class Command(BaseCommand):
    help = 'Populate database tables with random data.'

    def handle(self, *args, **kwargs):
        fake = Faker()

        addresses = []
        for _ in range(100000):
            addresses.append(Address(
                street = fake.street_name(),
                street_number=fake.building_number(),
                city_code=fake.zipcode(),
                city=fake.city(),
                country=fake.country(),
            ))
        # Bulk create of Address records
        Address.objects.bulk_create(addresses)
        address_ids = list(Address.objects.values_list('id', flat=True))

        appusers = []
        customer_relationships = []
        for _ in range(300000):
            # Randomly pick an address from the Address model
            address_id = random.choice(address_ids)
            
            appuser = AppUser(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender=random.choice(['Male', 'Female']),
                customer_id=fake.unique.uuid4(),
                phone_number=fake.phone_number(),
                address_id=address_id,
                birthday=fake.date_of_birth(),
            )
            appusers.append(appuser)
            customer_relationships.append(CustomerRelationship(
                appuser=appuser, # Mapping of AppUser model to appuser field
                points=random.randint(1, 10000),
                last_activity=fake.date_this_decade(),
            ))
        # Bulk create of AppUser records
        AppUser.objects.bulk_create(appusers)
        # Bulk create of CustomerRelationship records
        CustomerRelationship.objects.bulk_create(customer_relationships)
        self.stdout.write(self.style.SUCCESS('Data population in database tables completed successfully.'))


