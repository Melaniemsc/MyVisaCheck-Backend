from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status

from .models import Country
from .serializer.common import CountrySerializer
from country_to_travel.models import CountryToTravel
from types_of_visa.models import Visa
from rest_framework.exceptions import NotFound
from .seeder import load_visa_requirements, load_countries
from rest_framework.permissions import IsAdminUser
from project.custom_permissions import IsAdminOrReadOnly


class CountrylistView(APIView):
    permission_classes = (IsAdminOrReadOnly, )
    def get(self, _request):
        countries = Country.objects.all()
        serialized_countries = CountrySerializer(countries, many=True)
        return Response(serialized_countries.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        country_to_add = CountrySerializer(data = request.data)
        if country_to_add.is_valid():
            country_to_add.save()
            return Response(country_to_add.data, status=status.HTTP_201_CREATED)
        return Response (country_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CountryDetailView(APIView):
    permission_classes = (IsAdminOrReadOnly, )

    def get_country (self, name):
      return Country.objects.get(name=name)

    
    def get (self, _request, name):
        try:
            country = self.get_country(name=name)
            serialized_country = CountrySerializer(country)
            return Response (serialized_country.data, status=status.HTTP_200_OK)
        except Country.DoesNotExist:
            raise NotFound(detail="Country not found")
    
    def put(self, request, name):
        country_to_edit = self.get_country(name=name)
        
        updated_country = CountrySerializer(country_to_edit, data=request.data) 
        if updated_country.is_valid():
            updated_country.save()
            return Response(updated_country.data, status=status.HTTP_202_ACCEPTED)
        
        return Response (updated_country.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    def delete (self, _request, name):
        country_to_delete = self.get_country(name=name)
        country_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  


class CountryVisaRequirement(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request):
        load_visa_requirements();
        return Response("Country Visa Requirement Generated", status=status.HTTP_201_CREATED)

class CountrysSeed(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request):
        load_countries();
        return Response("Countries generated", status=status.HTTP_201_CREATED)



class Visa_requirement:
    def __init__(self, country, visa_requirement, allowed_stay, notes):
        self.country = country
        self.visa_requirement = visa_requirement
        self.allowed_stay = allowed_stay     
        self.notes = notes
