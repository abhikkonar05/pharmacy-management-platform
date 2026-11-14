
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import home

urlpatterns = [
    path("", home, name="home"),

    path("admin/", admin.site.urls),

    path("api/health/", include("health.urls")),
    path("api/medicines/", include("medicines.urls")),
    path("api/batches/", include("batches.urls")),
    path("api/stock-movements/", include("stock.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/auth/token/", obtain_auth_token, name="api-token"),
]

