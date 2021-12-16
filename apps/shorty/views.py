from django.urls import reverse
from django.core.cache import cache
from django.views import generic

from .models import Shorty
from .forms import CreateLinkForm, EditLinkForm
from .utils import get_link


class HomeView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CreateLinkForm()
        })
        return context


class LinkListVIew(generic.ListView):
    model = Shorty
    ordering = '-timestamp'
    template_name = 'links/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(session__session_key=self.request.session.session_key)


class CreateLinkView(generic.CreateView):
    model = Shorty
    form_class = CreateLinkForm
    template_name = 'forms/create_link.html'

    def form_valid(self, form):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        form.instance.session = self.request.session._get_session_from_db()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


class UpdateLinkView(generic.UpdateView):
    model = Shorty
    slug_field = 'link'
    slug_url_kwarg = 'link'
    form_class = EditLinkForm
    template_name = 'forms/edit_link.html'

    def get_success_url(self):
        return reverse('load_link_list')


class RedirectToUrlView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        kwargs.clear()
        url = cache.get(self.kwargs.get('link'))
        if url:
            self.url = url
        else:
            self.pattern_name = 'index'
        return super().get_redirect_url(*args, **kwargs)
