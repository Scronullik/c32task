from django import forms


class ShortenForm(forms.Form):
    url = forms.URLField(label='', widget=forms.URLInput(attrs={'placeholder': 'Shorten your link'}))
