import pytest
from rest_framework.test import APIClient

from teams.models import Memberships, Team
from users.models import User
from projects.models import Project


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
def team(owner, member):
    team = Team.objects.create(name="Backend", owner=owner)
    Memberships.objects.create(user=owner, team=team, role=Memberships.Role.OWNER)
    Memberships.objects.create(user=member, team=team, role=Memberships.Role.MEMBER)
    return team

@pytest.fixture
def project(team):
    return Project.objects.create(name="Project 1", description="Test project", team=team)