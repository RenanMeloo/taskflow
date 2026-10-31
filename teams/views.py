from django.shortcuts import render
from rest_framework import viewsets
from .models import Team, Memberships
from .serializers import TeamSerializer, MembershipSerializer
import rest_framework.permissions as permissions
from .permission import TeamPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class TeamViewSet(viewsets.ModelViewSet):
    # define which serializer to use for this viewset
    serializer_class = TeamSerializer
    permission_classes = [TeamPermission, IsAuthenticated]

    def get_queryset(self):
        # list teams that the current user is a member of
        return Team.objects.filter(memberships__user=self.request.user)

    def perform_create(self, serializer):
        # set owner of the team to the current user
       team = serializer.save(owner=self.request.user)
       Memberships.objects.create(
           user=self.request.user, 
           team=team, 
           role=Memberships.Role.OWNER)

    @action(detail=True, methods=["get", "post"])
    def members(self, request, pk=None):
        team = self.get_object()

        if request.method == "GET":
            serializer = MembershipSerializer(team.memberships.all(), many=True)
            return Response(serializer.data)

        serializer = MembershipSerializer(data=request.data,context={"team": team})
        serializer.is_valid(raise_exception=True)
        serializer.save(team=team)
        return Response(serializer.data, status=201)