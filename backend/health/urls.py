
from django.urls import path

from .views import liveness_check, readiness_check


urlpatterns = [
    path("", readiness_check, name="health-check"),
    path("live/", liveness_check, name="liveness-check"),
    path("ready/", readiness_check, name="readiness-check"),
]
