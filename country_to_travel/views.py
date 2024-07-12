from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404
import requests
from bs4 import BeautifulSoup
import pandas as pd
from country_to_travel.models import CountryToTravel
from types_of_visa.models import Visa

from countries.models import Country
from .models import CountryToTravel
from .serializer.populated import PopulatedCountryToTravelSerializer
from rest_framework.permissions import IsAdminUser, IsAdminOrReadOnly


class CountryToTravelView(APIView):
    permission_classes = (IsAdminOrReadOnly, )
    def get(self, request):
        country_from = request.query_params.get('country_from')
        country_from_list = country_from.split(',')

        countries = get_list_or_404(Country, name__in=country_from_list)
        country_id = [country.id for country in countries]
        countries_to_travel = CountryToTravel.objects.filter(country_from__in = country_id)
        serialized_countries_to_travel = PopulatedCountryToTravelSerializer(countries_to_travel, many=True)

        return Response(serialized_countries_to_travel.data, status=status.HTTP_200_OK)
    

    def post(self, _request):
        (name,nationality) = self.extract_country_data()

        country = Country.objects.get_or_create(name=name, defaults={'nationality': nationality})
        
        visa_requirement = self.fetch_
    
        country_to = Country.objects.get(name=visa_requirement.country)

        new_country_to_travel = CountryToTravel(
            country_from=country, 
            country_to=country_to, 
            allowed_stay=visa_requirement.allowed_stay, 
            notes=visa_requirement.notes
        )
        new_country_to_travel.save()

        
        if '/' in visa_requirement.visa_requirement:
            visa_types = visa_requirement.visa_requirement.split(' / ')
            for visa_type in visa_types:
                visa = Visa.objects.get_or_create(type=visa_type)
                new_country_to_travel.visa_type.add(visa.pk)
        else:
            visa = Visa.objects.get_or_create(type=visa_requirement.visa_requirement)
            print(visa.pk)
            new_country_to_travel.visa_type.add(visa.pk)

        new_country_to_travel.save()
        return Response("new country and visa relations created",status=status.HTTP_201_CREATED)
    

    def fetch_data(self):
        response = requests.get("https://en.m.wikipedia.org/wiki/Visa_requirements_for_Venezuelan_citizens")
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def fetch_data_from_wiki(self,url):
        response = requests.get('https://en.m.wikipedia.org' + url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def extract_country_data(self):
        soup_visa_requirement = self.fetch_data()

        country_link = soup_visa_requirement.select_one('section p a[href^="/wiki/"]')
        country_wiki_url = country_link['href']
        name = country_wiki_url.split('/')[-1].replace('_', ' ')
        
        print("Name: " + name)
        
        soup_country = self.fetch_data_from_wiki(country_wiki_url)
        nationality = soup_country.select_one('#mf-section-0 > table > tbody > tr:nth-child(11) > td > a').text.strip()

        print("Name: "+ name + " Nationality: " + nationality)

        return (name,nationality)
        

class Visa_requirement:
    def __init__(self, country, visa_requirement, allowed_stay, notes):
        self.country = country
        self.visa_requirement = visa_requirement
        self.allowed_stay = allowed_stay     
        self.notes = notes
