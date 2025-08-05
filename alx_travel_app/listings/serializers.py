from rest_framework import serializers
from listings import models


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Property
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = '__all__'