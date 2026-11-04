from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .permissions import ProjectPermission
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        # Users only see projects of teams they belong to
        return Project.objects.filter(team__memberships__user=self.request.user)