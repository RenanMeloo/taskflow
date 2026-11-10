from rest_framework import permissions

from teams.models import Membership


class TaskPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Any team member can read
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == "destroy":
            # The creator can always delete their task
            if obj.created_by == request.user:
                return True

            # If the creator is still in the team, only they can delete it
            team = obj.project.team
            creator_is_member = team.memberships.filter(user=obj.created_by).exists()
            if creator_is_member:
                return False

            # Orphan task: owners and admins can delete it
            return team.memberships.filter(
                user=request.user,
                role__in=[Membership.Role.OWNER, Membership.Role.ADMIN],
            ).exists()

        # Any team member can edit
        return obj.project.team.memberships.filter(user=request.user).exists()