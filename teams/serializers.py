from rest_framework import serializers

from teams.models import Memberships, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "id", "name", "description", "created_at", "owner"
        read_only_fields = ("owner", "created_at")


class MembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Memberships
        fields = ["id", "user", "username", "team", "role", "joined_at"]
        read_only_fields = ("joined_at", "team")

    def validate_user(self, value):
        team = self.context["team"]
        if Memberships.objects.filter(team=team, user=value).exists():
            raise serializers.ValidationError(
                "This user is already a member of this team."
            )

        if value == Memberships.Role.OWNER:
            raise serializers.ValidationError("You cannot assign the owner role.")
        return value
