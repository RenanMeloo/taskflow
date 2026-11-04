from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermission
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]

    def get_queryset(self):
        # Return tasks that belong to projects where the user is a member of the team
        user = self.request.user
        return Task.objects.filter(project__team__memberships__user=user)

    @action(detail=True, methods=["get", "post"])
    def comments(self, request,pk=None):
        task = self.get_object()

        if request.method == "GET":
            comments = task.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    