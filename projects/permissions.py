from rest_framework import permissions

from teams.models import Memberships


class ProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Any team member can read
        if request.method in permissions.SAFE_METHODS:
            return True

        # check if the user is an admin or owner of the team
        return Memberships.objects.filter(
            user=request.user,
            team=obj.team,
            role__in=[Memberships.Role.ADMIN, Memberships.Role.OWNER],
        ).exists()
