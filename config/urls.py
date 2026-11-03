from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/", include("teams.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("projects.urls")),
    path("api/", include("tasks.urls")),
]
