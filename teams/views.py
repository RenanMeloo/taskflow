from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Membership, Team
from .permissions import TeamPermission
from .serializers import MembershipSerializer, TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    def get_queryset(self):
        # Users only see teams they belong to
        return Team.objects.filter(memberships__user=self.request.user)

    def perform_create(self, serializer):
        # The creator becomes the team owner
        with transaction.atomic():
            team = serializer.save(owner=self.request.user)
            Membership.objects.create(
                user=self.request.user,
                team=team,
                role=Membership.Role.OWNER,
            )

    @action(detail=True, methods=["get", "post"])
    def members(self, request, pk=None):
        team = self.get_object()

        if request.method == "GET":
            serializer = MembershipSerializer(team.memberships.all(), many=True)
            return Response(serializer.data)

        serializer = MembershipSerializer(data=request.data, context={"team": team})
        serializer.is_valid(raise_exception=True)
        serializer.save(team=team)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path=r"members/(?P<user_id>\d+)")
    def remove_member(self, request, pk=None, user_id=None):
        team = self.get_object()
        membership = get_object_or_404(Membership, team=team, user_id=user_id)

        if membership.role == Membership.Role.OWNER:
            return Response(
                {"detail": "You cannot remove the owner of the team."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
