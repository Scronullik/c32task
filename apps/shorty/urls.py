from django.urls import path

from .views import home, redirect_to_url

urlpatterns = [
    path('',  home, name='index'),
    path('<str:subpart>', redirect_to_url, name='redirect_to_url')
]
