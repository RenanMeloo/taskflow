from django.db.models import Case, IntegerField, Value, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .permissions import TaskPermission
from .serializers import CommentSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["status", "priority", "assignee", "project", "created_by"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at", "updated_at", "priority_level"]

    def get_queryset(self):
        # Users only see tasks from their teams' projects
        return Task.objects.filter(
            project__team__memberships__user=self.request.user
        ).annotate(
            priority_level=Case(
                When(priority=Task.Priority.LOW, then=Value(1)),
                When(priority=Task.Priority.MEDIUM, then=Value(2)),
                When(priority=Task.Priority.HIGH, then=Value(3)),
                output_field=IntegerField(),
            )
        )

    @action(detail=True, methods=["get", "post"], serializer_class=CommentSerializer)
    def comments(self, request, pk=None):
        task = self.get_object()

        if request.method == "GET":
            comments = task.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
