from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password
import uuid

# Create your models here.

"""user_id (Primary Key, UUID, Indexed)
first_name (VARCHAR, NOT NULL)
last_name (VARCHAR, NOT NULL)
email (VARCHAR, UNIQUE, NOT NULL)
password_hash (VARCHAR, NOT NULL)
phone_number (VARCHAR, NULL)
role (ENUM: 'guest', 'host', 'admin', NOT NULL)
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)"""

role_choices = {
    'guest': 'guest',
    'host': 'host',
    'admin': 'admin'
}
class User(AbstractUser):
    user_id= models.UUIDField(default= uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(max_length=55, unique=True, null=False, blank=True, db_index=True)
    password_hash= models.CharField(max_length=99, null=False)
    phone_number= models.CharField(max_length=15, null=False)
    role= models.CharField(max_length=15, choices=role_choices, null=False, blank=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password_hash.startswith('pbkdf2_'):
            self.password_hash = make_password(self.password_hash)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name}"
    

"""property_id: Primary Key, UUID, Indexed
host_id: Foreign Key, references User(user_id)
name: VARCHAR, NOT NULL
description: TEXT, NOT NULL
location: VARCHAR, NOT NULL
pricepernight: DECIMAL, NOT NULL
created_at: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
updated_at: TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP"""

class Property(models.Model):
    property_id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    host_id= models.ForeignKey(User, on_delete=models.CASCADE, related_name='property')
    name= models.CharField(max_length=255, null=False)
    description= models.TextField(null=False)
    location= models.CharField(max_length=255, null=False)
    pricepernight= models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


"""booking_id: Primary Key, UUID, Indexed
property_id: Foreign Key, references Property(property_id)
user_id: Foreign Key, references User(user_id)
start_date: DATE, NOT NULL
end_date: DATE, NOT NULL
total_price: DECIMAL, NOT NULL
status: ENUM (pending, confirmed, canceled), NOT NULL
created_at: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP"""

status_choices= {
    'pending': 'pending',
    'confirmed': 'confirmed',
    'canceled': 'canceled'
}
class Booking(models.Model):
    booking_id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    property_id= models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings', db_index=True)
    user_id= models.ForeignKey(User, on_delete= models.CASCADE, related_name='booking')
    start_date= models.DateField(null=False)
    end_date= models.DateField(null=False)
    total_price= models.DecimalField(max_digits=10, decimal_places=2, null=False)
    status= models.CharField(max_length=55, choices=status_choices, null=False, blank=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_id} {self.total_price}"


"""payment_id: Primary Key, UUID, Indexed
booking_id: Foreign Key, references Booking(booking_id)
amount: DECIMAL, NOT NULL
payment_date: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
payment_method: ENUM (credit_card, paypal, stripe), NOT NULL"""

payment_methods={
    'credit_card': 'credit_card',
    'paypal': 'paypal',
    'stripe': 'stripe'
}
class Payment(models.Model):
    payment_id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    booking_id= models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payment', db_index=True)
    amount= models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_date= models.DateTimeField(auto_now_add=True)
    payment_method= models.CharField(max_length=55, choices=payment_methods, null=False, blank=False)

    def __str__(self):
        return f"{self.booking_id} {self.amount}"


"""review_id: Primary Key, UUID, Indexed
property_id: Foreign Key, references Property(property_id)
user_id: Foreign Key, references User(user_id)
rating: INTEGER, CHECK: rating >= 1 AND rating <= 5, NOT NULL
comment: TEXT, NOT NULL
created_at: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP"""

class Review(models.Model):
    review_id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    property_id= models.ForeignKey(Property, on_delete=models.CASCADE)
    user_id= models.ForeignKey(User, on_delete=models.CASCADE)
    rating= models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment= models.TextField(null=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_id}"
