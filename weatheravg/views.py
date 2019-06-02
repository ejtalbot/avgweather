from .forms import WeatherForm
from django.views.generic.edit import FormView
from django.http import JsonResponse
import requests
from django.conf import settings

class WeatherView(FormView):
    template_name = 'weatheravg/weatherform.html'
    form_class = WeatherForm
    success_url = '/weatheravg/'

    def form_valid(self, form):
        totalTemp = 0
        googleUrl = "https://maps.googleapis.com/maps/api/geocode/json"
        googleParams={}
        googleParams['key'] = settings.GOOGLE_MAPS_KEY
        providers = form.cleaned_data["providers"]
        if form.cleaned_data['location_mode'] == 'latlng':
            latitude = form.cleaned_data["latitude"]
            longitude = form.cleaned_data["longitude"]
            #latlng validation
            googleLatlng = '%s,%s' % (latitude, longitude)
            googleParams['latlng'] = googleLatlng
            googleResponse = requests.get(url=googleUrl, params=googleParams).json()
            if googleResponse['status'] != "OK":
                response = {'error': 'Unable to validate latlng'}
                return JsonResponse(response)
        #Convert zipcode to latlng 
        else:
            postal_code = form.cleaned_data["zipcode"]
            googleParams['components'] = 'postal_code:%s' % (postal_code)
            googleResponse = requests.get(url=googleUrl, params=googleParams).json()
            if googleResponse['status'] != "OK":
                response = {'error': 'Unable to convert zipcode to latlng'}
                return JsonResponse(response)
            else:
                latitude = googleResponse['results'][0]['geometry']['location']['lat']
                longitude = googleResponse['results'][0]['geometry']['location']['lng']
        #loop through wetaher providers to get temperature
        for provider in providers:
            if provider == 'accuweather':
                accuUrl = 'http://127.0.0.1:5000/accuweather'
                accuParams={}
                accuParams['latitude'] = latitude
                accuParams['longitude'] = longitude
                accuResponse = requests.get(url=accuUrl, params=accuParams)
                totalTemp += float(accuResponse.json()["simpleforecast"]["forecastday"][0]["current"]["fahrenheit"])
            elif provider == 'noaa':
                noaaUrl = 'http://127.0.0.1:5000/noaa'
                noaaParams = {}
                noaaParams['latlon'] = '%s,%s' % (latitude, longitude)
                noaaResponse = requests.get(url=noaaUrl, params=noaaParams)
                totalTemp += float(noaaResponse.json()["today"]["current"]["fahrenheit"])
            elif provider == 'weatherdotcom':
                weatherUrl = 'http://127.0.0.1:5000/weatherdotcom'
                weatherData = {}
                weatherData['lat'] = latitude
                weatherData['lon'] = longitude
                weatherResponse = requests.post(url=weatherUrl, json=weatherData)
                totalTemp += float(weatherResponse.json()["query"]["results"]["channel"]["condition"]["temp"])
        averageTemp = totalTemp / len(providers)
        response = {'averageTemperature': averageTemp}
        return JsonResponse(response)