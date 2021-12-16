from django import forms
from django.core.cache import cache

from .models import Shorty
# from .utils import get_link


class CreateLinkForm(forms.ModelForm):

    class Meta:
        model = Shorty
        fields = ('url', )
        labels = {
            'url': '',
        }
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Shorten your link'}),
        }

    def save(self, commit=True):
        self.instance = super().save(commit=commit)
        cache.set(self.instance.link, self.instance.url)
        return self.instance


class EditLinkForm(forms.ModelForm):
    class Meta:
        model = Shorty
        fields = ('link',)
        labels = {
            'link': '',
        }
        widgets = {
            'link': forms.TextInput(attrs={'placeholder': 'your link'})
        }
