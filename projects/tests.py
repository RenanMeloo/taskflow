import pytest

from projects.models import Project
from users.models import User
from tasks.models import Task


@pytest.mark.django_db
def test_owner_can_create_project(api_client, owner, team):
    api_client.force_authenticate(user=owner)

    response = api_client.post("/api/projects/", {"name": "Site novo", "team": team.id})

    assert response.status_code == 201
    assert Project.objects.filter(name="Site novo", team=team).exists()

@pytest.mark.django_db
def test_member_cannot_create_project(api_client, member, team):
    api_client.force_authenticate(user=member)

    response = api_client.post("/api/projects/", {"name": "Site novo", "team": team.id})

    assert response.status_code == 400
    assert not Project.objects.filter(name="Site novo", team=team).exists()

@pytest.mark.django_db
def test_member_cannot_edit_project(api_client, member, team):
    project = Project.objects.create(name="Site novo", team=team)

    api_client.force_authenticate(user=member)

    response = api_client.put(f"/api/projects/{project.id}/", {"name": "Site editado", "team": team.id})

    assert response.status_code == 403
    assert not Project.objects.filter(name="Site editado", team=team).exists()

@pytest.mark.django_db
def test_unauthorized_user_cannot_list_projects(api_client, team):
    response = api_client.get("/api/projects/")

    assert response.status_code == 401

@pytest.mark.django_db
def test_outsider_cannot_see_project(api_client, team):
    project = Project.objects.create(name="Site novo", team=team)
    outsider = User.objects.create_user(username="outsider", email="outsider@test.com", password="pass12345")
    api_client.force_authenticate(user=outsider)

    list_response = api_client.get("/api/projects/")
    assert list_response.status_code == 200
    assert len(list_response.data["results"]) == 0

    detail_response = api_client.get(f"/api/projects/{project.id}/")
    assert detail_response.status_code == 404

