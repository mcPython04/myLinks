from django import forms
from .models import link


class CreateLinkForm(forms.Form):
    hyperlink = forms.URLField()
    website_name = forms.CharField()
    #image = forms.ImageField()
    def end_form(self):
        pass
