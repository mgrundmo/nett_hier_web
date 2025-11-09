from cloudinary.forms import CloudinaryFileField
from django import forms
from .models import Location, Countries

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['country', 'city', 'latitude', 'longitude', 'sticker_img']

    country = forms.ModelChoiceField(
        queryset=Countries.objects.all(),
        to_field_name='name',
        required=True,
        widget=forms.Select(attrs={'class':'form-select', 'style': 'width:400px'})
    )

    sticker_img = CloudinaryFileField()
