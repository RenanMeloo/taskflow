import pytest
from rest_framework.test import APIClient

from projects.models import Project
from teams.models import Membership, Team
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def owner():
    return User.objects.create_user(username="owner", email="owner@test.com", password="pass12345")


@pytest.fixture
def member():
    return User.objects.create_user(username="member", email="member@test.com", password="pass12345")


@pytest.fixture
def admin():
    return User.objects.create_user(username="admin", email="admin@test.com", password="pass12345")


@pytest.fixture
def team(owner, admin, member):
    team = Team.objects.create(name="Backend", owner=owner)
    Membership.objects.create(user=owner, team=team, role=Membership.Role.OWNER)
    Membership.objects.create(user=admin, team=team, role=Membership.Role.ADMIN)
    Membership.objects.create(user=member, team=team, role=Membership.Role.MEMBER)
    return team


@pytest.fixture
def project(team):
    return Project.objects.create(name="Project 1", description="Test project", team=team)
