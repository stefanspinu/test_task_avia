from django.shortcuts import render
from django.template.defaulttags import register
from django.core.paginator import Paginator

import requests

from decouple import config

from .models import Aircraft
from .filters import AircraftFilter

# Create your views here.

API_TOKEN = config("API_TOKEN")

@register.filter()
def split(value, key):
    return value.split(key)


def get_aircrafts():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': API_TOKEN}
    response = requests.get('https://dir.aviapages.com/api/aircraft/?images=True', headers=headers).json()

    aircrafts = response['results']

    for aircraft in aircrafts:
        a_company_data = aircraft['company_name']
        a_airport_data = aircraft['home_base']
        aircraft_company = requests.get(f'https://dir.aviapages.com/api/companies/?search_name={a_company_data}', headers=headers).json()
        aircraft_airport = requests.get(f'https://dir.aviapages.com/api/airports/?search_icao={a_airport_data}', headers=headers).json()

        a, created = Aircraft.objects.get_or_create(tail_number=aircraft['tail_number'], serial_number=aircraft['serial_number'], aircraft_type=aircraft['aircraft_type_name'], year_of_production=aircraft['year_of_production'], aircraft_class=aircraft['aircraft_class_name'])

        for aircraft_comp in aircraft_company['results']:
            a.company_name = aircraft_comp['name']
            a.company_phone = aircraft_comp['phone']
            a.company_website = aircraft_comp['website']
            a.save()

        for aircraft_airp in aircraft_airport['results']:
            a.IATA = aircraft_airp['iata']
            a.ICAO = aircraft_airp['icao']
            a.airport_name = aircraft_airp['name']
            a.save()
                
        if aircraft['images']:
            a.images = ''
            count = 0
            for img in aircraft['images'][:3]:
                if count == 0:
                    a.images = a.images + img['url']
                else:
                    a.images = a.images + ',' + img['url']
                a.save()
                count = count + 1


def home(request):
    # get_aircrafts()
    all_aircrafts = Aircraft.objects.all()
    aircrafts_filter = AircraftFilter(request.GET, queryset=all_aircrafts)
    all_aircrafts = aircrafts_filter.qs
    paginator = Paginator(all_aircrafts, 300)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'aircrafts': all_aircrafts,
        'aircrafts_filter': aircrafts_filter,
        'page_obj': page_obj
    }
    return render(request, 'main/index.html', context)

