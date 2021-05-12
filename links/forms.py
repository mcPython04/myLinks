from django import forms
from .models import link, collection


# Our own create collection form
class CreateCollectionForm(forms.ModelForm):

    # Grants access to request object so that only links of the current user are given as options
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
        required=False,
        queryset=None,
    )


# Our own update collection form
class UpdateCollectionForm(forms.ModelForm):

    # Grants access to request object so that only links of the current user are given as options
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UpdateCollectionForm, self).__init__(*args, **kwargs)
        self.fields['links'].queryset = link.objects.filter(user=self.request.user)

    class Meta:
        model = collection
        fields = ['links']

    links = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
        queryset=None,
    )
