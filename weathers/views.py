import os.path
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import City
from .forms import CityCreate
import requests
import json

BASE = os.path.dirname(os.path.abspath(__file__))

api_endpoint = 'https://api.openweathermap.org/data/2.5'
view_my_cities = requests.get("https://simplemaps.com/data/my-cities")
fetch_city_weather = None
fetch_city_forecast = requests.get(f"{api_endpoint}/forecast")

def index(request):
    try:
        file = open(os.path.join(BASE, "my_cities.json"), "r")
        cities = json.load(file)
        return render(request, "weather/index.html", {
            "cities": cities,
        })
    except:
        return HttpResponseNotFound("File is empty")
    
def view_cities(request):
    try:
        cities = City.objects.all()
        return render(request, 'weather/cities.html', {'cities': cities})
    except:
        return HttpResponseNotFound("No Data Available")
    
def create_city(request):
    upload = CityCreate()
    if request.method == 'POST':
        city = CityCreate(request.POST)
        if city.is_valid():
            city.save()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'weather/create_city.html', {'upload_form':upload})

def update_city(request, city_id):
    city_id = int(city_id)
    try:
        city_sel = City.objects.get(id = city_id)
    except City.DoesNotExist:
        return redirect('index')
    upload_form = CityCreate(request.POST or None, instance = city_sel)
    if upload_form.is_valid():
       upload_form.save()
       return redirect('index')
    return render(request, 'weather/create_city.html', {'upload_form':upload_form})

def delete_city(request, city_id):
    city_id = int(city_id)
    try:
        city_sel = City.objects.get(id = city_id)
    except City.DoesNotExist:
        return redirect('index')
    city_sel.delete()
    return redirect('index')

def city_weather(request, city):
    fetch_city_weather = requests.get(f"{api_endpoint}/weather?q={city}&appid=ef1564f9c31c019b6139c9da08aa259f")
    data = fetch_city_weather.json()
    return render(request, "weather/weather.html", {
        "data": [data],
    })

def city_forecast(request, city):
    forecast_list = []
    fetch_city_weather = requests.get(f"{api_endpoint}/forecast?q={city}&appid=ef1564f9c31c019b6139c9da08aa259f")
    data = fetch_city_weather.json()
    for list in data["list"]:
        if len(forecast_list) < 5:
            forecast_list.append(list)
        
    return render(request, "weather/forecast.html", {
        "data": forecast_list,
    })
