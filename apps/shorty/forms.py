from django import forms

from .models import Shorty


class CreateLinkForm(forms.ModelForm):
    class Meta:
        model = Shorty
        fields = ('url',)
        labels = {
            'url': '',
        }
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Shorten your link'}),
        }


class EditLinkForm(forms.ModelForm):
    class Meta:
        model = Shorty
        fields = ('link',)
        labels = {
            'link': '',
        }
        widgets = {
            'link': forms.TextInput(attrs={'placeholder': 'your link'}),
        }
