from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware


class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)
        if not request.session.exists(request.session.session_key):
            request.session.create()
