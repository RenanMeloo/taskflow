from rest_framework import serializers

from teams.models import Memberships

from .models import Comment, Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "project",
            "assignee",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_project(self, value):
        # Only members of the project's team can add tasks to it
        user = self.context["request"].user
        if not Memberships.objects.filter(user=user, team=value.team).exists():
            raise serializers.ValidationError(
                "You are not a member of this project's team."
            )
        return value

    def validate(self, attrs):
        # On partial updates the project may not be sent, so fall back to the current one
        project = attrs.get("project") or self.instance.project
        assignee = attrs.get("assignee")

        if (
            assignee
            and not Memberships.objects.filter(
                user=assignee, team=project.team
            ).exists()
        ):
            raise serializers.ValidationError(
                {"assignee": "The assignee must be a member of the project's team."}
            )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "task", "author", "author_username", "content", "created_at"]
        read_only_fields = ["task", "author", "created_at"]
