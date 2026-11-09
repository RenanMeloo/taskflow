from rest_framework import permissions

from teams.models import Membership


class ProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Any team member can read
        if request.method in permissions.SAFE_METHODS:
            return True

        # check if the user is an admin or owner of the team
        return Membership.objects.filter(
            user=request.user,
            team=obj.team,
            role__in=[Membership.Role.ADMIN, Membership.Role.OWNER],
        ).exists()
