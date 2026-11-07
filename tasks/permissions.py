from rest_framework import permissions


class TaskPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # check permission methods for the task object
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == "destroy":
            # only the creator of the task can delete it
            return obj.created_by == request.user

        # check if the user is a member of the team associated with the task's project
        return obj.project.team.memberships.filter(user=request.user).exists()
