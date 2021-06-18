from django import forms
from .models import City
#DataFlair

class CityCreate(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'