from django import forms

class WeatherForm(forms.Form):
	#list out fields here
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    PROVIDERS = (
            ('accuweather', 'accuweather'),
            ('noaa', 'noaa'),
            ('weatherdotcom', 'weather.com')
        )
    providers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PROVIDERS)
    zipcode = forms.CharField(min_length=5, max_length=5, required=False)
    LOCATION_MODES = (
            ('latlng', 'Use latitude and longitude'),
            ('zipcode', 'Use zipcode')
    	)
    location_mode = forms.ChoiceField(choices=LOCATION_MODES)

    def clean(self):
    	#Make sure correct location type is provided based on mode
        cleaned_data = super(WeatherForm, self).clean()
        if cleaned_data['location_mode'] == 'latlng' and (not cleaned_data['latitude'] or not cleaned_data['longitude']): 
            raise forms.ValidationError('Please fill in latitude and longitude')
        if cleaned_data['location_mode'] == 'zipcode' and not cleaned_data['zipcode']: 
            raise forms.ValidationError('Please fill in zipcode')