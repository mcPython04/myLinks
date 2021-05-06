from django import forms
from .models import link, collection


class CreateCollectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')
        super(CreateCollectionForm, self).__init__(*args, **kwargs)
        self.fields['links'].queryset = link.objects.filter(user=self.request.user)

    class Meta:
        model = collection
        fields = ['name', 'links']

    name = forms.CharField()
    links = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=None
    )
