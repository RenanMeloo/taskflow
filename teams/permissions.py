from rest_framework import permissions

from .models import Membership


class TeamPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # check permission methods for the team object
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == "destroy":
            # only the owner can delete the team
            return obj.owner == request.user

        # check if the user is an admin or owner of the team
        return Membership.objects.filter(
            user=request.user,
            team=obj,
            role__in=[Membership.Role.ADMIN, Membership.Role.OWNER],
        ).exists()
