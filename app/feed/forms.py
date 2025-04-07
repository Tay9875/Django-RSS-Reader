from django import forms
from django.forms import ModelForm
from .models import Feed

class RssForm(ModelForm):
    url = forms.TextInput()
    class Meta:
        model = Feed
        fields =['url']