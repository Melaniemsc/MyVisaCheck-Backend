from .common import CountryToTravelSerializer
from countries.serializer.common import CountrySerializer
from types_of_visa.serializer.common import Type_of_VisaSerializer

class PopulatedCountryToTravelSerializer(CountryToTravelSerializer):
  country_from = CountrySerializer()
  country_to = CountrySerializer()
  visa_type = Type_of_VisaSerializer(many=True)