from django.urls import path, include

from apps.shorty.api.urls import router as shorty_router

from .routers import DefaultRouter


router = DefaultRouter()
router.extend(shorty_router)


urlpatterns = [
    path('',            include(router.urls)),
    path('auth/',       include('rest_framework.urls')),
]
