
from rest_framework import permissions
from .models import Memberships

class TeamPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #chech permission methods for the team object
        if request.method in permissions.SAFE_METHODS:
            return True

        # check if the user is a member of the team
        return Memberships.objects.filter(
            user=request.user, 
            team=obj,
            role__in=[Memberships.Role.ADMIN, Memberships.Role.OWNER]
            ).exists()