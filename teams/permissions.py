
from rest_framework import permissions
from .models import Memberships

class TeamPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # check permission methods for the team object
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == "destroy":
            # only the owner can delete the team
            return obj.owner == request.user

        # check if the user is an admin or owner of the team
        return Memberships.objects.filter(
            user=request.user, 
            team=obj,
            role__in=[Memberships.Role.ADMIN, Memberships.Role.OWNER]
        ).exists()