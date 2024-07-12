from rest_framework import serializers
from ..models import CountryToTravel

class CountryToTravelSerializer(serializers.ModelSerializer):
  class Meta:
    model = CountryToTravel
    fields = '__all__'