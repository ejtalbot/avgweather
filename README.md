# Weather Averaging Project

Calculate the average weather from different providers based on latlon or zipcode wth google maps validation 

### Setup

Used Python 3.6.7

Install library requirements
```
pip install -r requirements.txt
```
Add your Google Maps API key to the GOOGLE_MAPS_KEY variable in the settings.py file before running.

### Running

Start the mock weather flask server from mock-weater-api

Start the django server (Default address and port 127.0.0.1:8000)
```
python manage.py runserver
```

Use app by navigating to http://127.0.0.1:8000/weatheravg/ to enter values and submit form for a json response.