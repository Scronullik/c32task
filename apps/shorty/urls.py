from django.urls import path, include

from .views import HomeView, LinkListVIew, CreateLinkView, UpdateLinkView, RedirectToUrlView

urlpatterns = [
    path('',  HomeView.as_view(), name='index'),
    path('<str:link>', RedirectToUrlView.as_view(), name='redirect_to_url'),
    path('ajax/', include([
        path('load_link_list', LinkListVIew.as_view(), name='load_link_list'),
        path('create_link', CreateLinkView.as_view(), name='create_link'),
        path('<str:link>/edit_link', UpdateLinkView.as_view(), name='edit_link'),
    ])),
]
