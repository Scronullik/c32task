from rest_framework.viewsets import ModelViewSet

from ..models import Shorty
from .serializers import ShortySerializer


class ShortyAPIViewSet(ModelViewSet):
    queryset = Shorty.objects.all()
    serializer_class = ShortySerializer

    def perform_create(self, serializer):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer.save(session=self.request.session._get_session_from_db())
