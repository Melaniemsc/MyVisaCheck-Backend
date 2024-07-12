import json
from functools import reduce
from .models import Country 
from country_to_travel.models import CountryToTravel
from types_of_visa.models import Visa
from .serializer.common import CountrySerializer
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.db.models import Q
import time
from io import StringIO

def load_countries():

    country_file_path = "./countrySeed.json"
    flags_file_path = "./countryInfo.json"

   
    with open(flags_file_path, 'r') as flags_file:
        flags_data = json.load(flags_file)
        
        flags_dict = {country['name']['common']: country['flags']['svg'] for country in flags_data}

   
    with open(country_file_path, 'r') as countries_file:
        countries_data = json.load(countries_file)

        for country_data in countries_data:
            country_name = country_data['name']

            existing_country = Country.objects.filter(name=country_name).first()

            if not existing_country:
                
                flag_url = flags_dict.get(country_name, None)
                if flag_url:
                    country_data['flag'] = flag_url  
                else:
                    print(f"Flag not found for country '{country_name}'")

                
                serializer = CountrySerializer(data=country_data)
                if serializer.is_valid():
                    serializer.save()
                    print(f"Created: Country '{country_name}'")
                else:
                    print(f"Error creating country '{country_name}': {serializer.errors}")
            else:
                print(f"Skipping: Country '{country_name}' already exists.")


def load_visa_requirements():
    countries = Country.objects.filter(name="Guinea-Bissauan")

    for country in countries:
        time.sleep(0.5)
        if (country.name=="Poland"):
            response = requests.get("https://en.wikipedia.org/wiki/Travel_requirements_for_Polish_citizens")
        if (country.name=="Guinea-Bissau"):
            response = requests.get("https://en.wikipedia.org/wiki/Visa_requirements_for_Guinea-Bissauan_citizens")
        if (country.name=="Luxembourg"):
            response = requests.get("https://en.wikipedia.org/wiki/Visa_requirements_for_citizens_of_Luxembourg")
        else:
            response = requests.get("https://en.m.wikipedia.org/wiki/Visa_requirements_for_"+formatCountry(country.nationality)+"_citizens")
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            dfs = [pd.read_html(StringIO(str(table)))[0] for table in tables]
            table_index = 0
            df_visa_requirement = dfs[table_index]

            while not ('Visa requirement' in df_visa_requirement or 'Entry requirement' in df_visa_requirement):
                table_index=table_index+1
                print('Country to modify => :' + country.name +" with index " + str(table_index))
                df_visa_requirement = dfs[table_index]

            if 'Country / Region' in df_visa_requirement:
                print('Country to modify => :' + country.name)
                df_visa_requirement = df_visa_requirement.rename({'Country / Region': 'Country'}, axis='columns')

            if 'Entry requirement' in df_visa_requirement:
                print('Country to modify => :' + country.name)
                df_visa_requirement = df_visa_requirement.rename({'Entry requirement': 'Visa requirement'}, axis='columns')

            if 'Stay duration' in df_visa_requirement:
                print('Country to modify => :' + country.name)
                df_visa_requirement = df_visa_requirement.rename({'Stay duration': 'Allowed stay'}, axis='columns')

            if 'Notes' in df_visa_requirement:
                print('Country to modify => :' + country.name)
                df_visa_requirement = df_visa_requirement.rename({'Notes': 'Notes (excluding departure fees)'}, axis='columns')

            if 'scope=col Notes (excluding departure fees)' in df_visa_requirement:
                print('Country to modify => :' + country.name)
                df_visa_requirement = df_visa_requirement.rename({'scope=col Notes (excluding departure fees)': 'Notes (excluding departure fees)'}, axis='columns')

            for column in df_visa_requirement.columns:
                df_visa_requirement[column] = df_visa_requirement[column].astype(str).str.replace(r'\[\d+\]', '', regex=True)

        # df_visa_requirement['Visa requirement'] = df_visa_requirement['Visa requirement'].str.split('/')
        
        # df_visa_requirement = df_visa_requirement.explode(['Visa requirement'])
    
        # df_visa_requirement['Visa requirement'] = df_visa_requirement['Visa requirement'].str.strip()

        # df_visa_requirement.to_csv('Poland.csv', index=False)
            for index, row in df_visa_requirement.iterrows():
                country_to = Country.objects.filter(name=row['Country']).first()
                if country_to is not None:
                    country_to_travel = CountryToTravel.objects.filter(country_from=country,country_to=country_to).first()
                    
                    if country_to_travel is None:
                        country_to_travel = CountryToTravel(country_from=country,country_to=country_to,allowed_stay=row['Allowed stay'],notes=row['Notes (excluding departure fees)'])
                        country_to_travel.save()

                    visa_requirements = row['Visa requirement'].split('/')
                    visa_requirements = [visa_requirement.strip() for visa_requirement in visa_requirements]
                    
                    q_list = map(lambda n: Q(type__iexact=n), visa_requirements)
                    q_list = reduce(lambda a, b: a | b, q_list)
                    visa_types = Visa.objects.filter(q_list)

                    country_to_travel.visa_type.add(*visa_types)
        except:
            df_visa_requirement.to_csv(country.nationality+'.csv', index=False)




# def load_visa_requirements():
#     countries = Country.objects.filter(name="Croatia")

#     for country in countries:
#         time.sleep(0.5)
#         if (country.name=="Poland"):
#             response = requests.get("https://en.wikipedia.org/wiki/Travel_requirements_for_Polish_citizens")
#         if (country.name=="Guinea-Bissau"):
#             response = requests.get("https://en.wikipedia.org/wiki/Visa_requirements_for_Guinea-Bissauan_citizens")
#         if (country.name=="Luxembourg"):
#             response = requests.get("https://en.wikipedia.org/wiki/Visa_requirements_for_citizens_of_Luxembourg")
#         else:
#             response = requests.get("https://en.m.wikipedia.org/wiki/Visa_requirements_for_"+formatCountry(country.nationality)+"_citizens")

#         soup = BeautifulSoup(response.content, 'html.parser')
#         tables = soup.find_all('table')
#         dfs = [pd.read_html(StringIO(str(table)))[0] for table in tables]
#         table_index = 0
#         df_visa_requirement = dfs[table_index]

#         while not ('Visa requirement' in df_visa_requirement or 'Entry requirement' in df_visa_requirement):
#             table_index=table_index+1
#             print('Country to modify => :' + country.name +" with index " + str(table_index))
#             df_visa_requirement = dfs[table_index]

#         if 'Country / Region' in df_visa_requirement:
#             print('Country to modify => :' + country.name)
#             df_visa_requirement = df_visa_requirement.rename({'Country / Region': 'Country'}, axis='columns')

#         if 'Entry requirement' in df_visa_requirement:
#             print('Country to modify => :' + country.name)
#             df_visa_requirement = df_visa_requirement.rename({'Entry requirement': 'Visa requirement'}, axis='columns')

#         if 'Stay duration' in df_visa_requirement:
#             print('Country to modify => :' + country.name)
#             df_visa_requirement = df_visa_requirement.rename({'Stay duration': 'Allowed stay'}, axis='columns')

#         if 'Notes' in df_visa_requirement:
#             print('Country to modify => :' + country.name)
#             df_visa_requirement = df_visa_requirement.rename({'Notes': 'Notes (excluding departure fees)'}, axis='columns')

#         if 'scope=col Notes (excluding departure fees)' in df_visa_requirement:
#             print('Country to modify => :' + country.name)
#             df_visa_requirement = df_visa_requirement.rename({'scope=col Notes (excluding departure fees)': 'Notes (excluding departure fees)'}, axis='columns')

#         for column in df_visa_requirement.columns:
#             df_visa_requirement[column] = df_visa_requirement[column].astype(str).str.replace(r'\[\d+\]', '', regex=True)

#     # df_visa_requirement['Visa requirement'] = df_visa_requirement['Visa requirement'].str.split('/')
    
#     # df_visa_requirement = df_visa_requirement.explode(['Visa requirement'])

#     # df_visa_requirement['Visa requirement'] = df_visa_requirement['Visa requirement'].str.strip()

#     # df_visa_requirement.to_csv('Poland.csv', index=False)
#         for index, row in df_visa_requirement.iterrows():
#             country_to = Country.objects.filter(name=row['Country']).first()
#             if country_to is not None:
#                 country_to_travel = CountryToTravel.objects.filter(country_from=country,country_to=country_to).first()
                
#                 if country_to_travel is None:
#                     country_to_travel = CountryToTravel(country_from=country,country_to=country_to,allowed_stay=row['Allowed stay'],notes=row['Notes (excluding departure fees)'])
#                     country_to_travel.save()

#                 visa_requirements = row['Visa requirement'].split('/')
#                 visa_requirements = [visa_requirement.strip() for visa_requirement in visa_requirements]
                
#                 q_list = map(lambda n: Q(type__iexact=n), visa_requirements)
#                 q_list = reduce(lambda a, b: a | b, q_list)
#                 visa_types = Visa.objects.filter(q_list)

#                 country_to_travel.visa_type.add(*visa_types)


        


def formatCountry(nationality):
    return nationality.replace(" ", "_");

class Visa_requirement:
    def __init__(self, country, visa_requirement, allowed_stay, notes):
        self.country = country
        self.visa_requirement = visa_requirement
        self.allowed_stay = allowed_stay     
        self.notes = notes
