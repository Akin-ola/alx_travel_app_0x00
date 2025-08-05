
from django.core.management import BaseCommand
from listings.models import Property
from django.contrib.auth import get_user_model
import uuid
from faker import Faker
import random



"""class Property(models.Model):
    property_id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    host_id= models.ForeignKey(User, on_delete=models.CASCADE, related_name='property')
    name= models.CharField(max_length=255, null=False)
    description= models.TextField(null=False)
    location= models.CharField(max_length=255, null=False)
    pricepernight= models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)"""

User = get_user_model()

fake = Faker()

class Command(BaseCommand):
    help= 'Seeds the database with initial data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding.....'))

        host_user, created = User.objects.get_or_create(
            username = 'host_user',
            defaults={'email': 'host_user@email.com', 'password':'hostpassword'} 
        )
        for i in range(20):
            Property.objects.create(
                host_id= host_user,
                name= fake.company(),
                description= fake.paragraph(nb_sentences=2),
                location= fake.city(),
                pricepernight= round(random.uniform(150.00, 500.00), 2)
            )