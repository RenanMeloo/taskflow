from django.contrib import admin

from .models import Memberships, Team

admin.site.register(Team)
admin.site.register(Memberships)
