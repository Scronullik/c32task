from django.shortcuts import render, redirect
from django.core.cache import cache

from .models import Shorty
from .forms import ShortenForm
from .utils import get_subpart


def home(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session_instance = request.session._get_session_from_db()
    if request.method == 'POST':
        form = ShortenForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            subpart = get_subpart()
            Shorty.objects.create(session=session_instance, url=url, subpart=subpart)
            cache.set(subpart, url)
            form = ShortenForm()
    else:
        form = ShortenForm()
    context = {
        'form': form,
        'shorty_list': session_instance.shorty_set.order_by('-timestamp')
    }
    return render(request, 'index.html', context)


def redirect_to_url(request, subpart):
    url = cache.get(subpart)
    if url:
        return redirect(url)
    else:
        return redirect('index')
