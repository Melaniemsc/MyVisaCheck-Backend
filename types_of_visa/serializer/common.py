from rest_framework import serializers
from ..models import Visa

class Type_of_VisaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Visa
    fields = '__all__'