from rest_framework import serializers

from teams.models import Membership

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "team", "created_at"]
        read_only_fields = ["created_at"]

    def validate_team(self, value):
        user = self.context["request"].user
        if not Membership.objects.filter(
            user=user,
            team=value,
            role__in=[Membership.Role.OWNER, Membership.Role.ADMIN],
        ).exists():
            raise serializers.ValidationError("You are not an owner or admin of this team.")
        return value
