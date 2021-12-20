from rest_framework.routers import DefaultRouter

from .views import ShortyAPIViewSet


router = DefaultRouter()
router.register('shorty', ShortyAPIViewSet)
