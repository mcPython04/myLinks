from django import forms
from .models import link, collection


class CreateCollectionForm(forms.ModelForm):

    class Meta:
        model = collection
        fields = ['name', 'links']

    name = forms.CharField()
    links = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=link.objects.all()
    )
