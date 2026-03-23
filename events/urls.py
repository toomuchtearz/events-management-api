from django.urls import path, include
from rest_framework import routers

from events.views import EventViewSet

app_name = "events"

router = routers.DefaultRouter()
router.register("", EventViewSet, basename="events")

urlpatterns = [
    path("", include(router.urls))
]
