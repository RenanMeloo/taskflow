import pytest

from projects.models import Project
from tasks.models import Task
from users.models import User

@pytest.mark.django_db
def test_member_can_create_task(api_client, member, project):
    api_client.force_authenticate(user=member)
    response = api_client.post("/api/tasks/", {"title": "Task 1", "description": "Test task", "project": project.id})
    assert response.status_code == 201
    task = Task.objects.get(title="Task 1")
    assert task.created_by == member

@pytest.mark.django_db
def test_outsider_cannot_see_task(api_client, project):
    # create a task in the project and an outsider user
    task = Task.objects.create(title="task 1", description="test task", project=project, created_by=project.team.owner)
    outsider = User.objects.create_user(username="outsider", email="outsider@example.com", password="pass12345")

    # force authenticate the outsider user and try to access the task list and detail endpoints
    api_client.force_authenticate(user=outsider)
    list_response = api_client.get("/api/tasks/")
    assert list_response.status_code == 200
    # check that the outsider user cannot see the task in the list response
    assert len(list_response.data["results"]) == 0
    # check that the outsider user cannot access the task detail endpoint
    detail_response = api_client.get(f"/api/tasks/{task.id}/")
    assert detail_response.status_code == 404

@pytest.mark.django_db
def test_non_creator_cannot_delete_task(api_client, owner, member, project):
    task = Task.objects.create(title="Task 1", project=project, created_by=member)
    api_client.force_authenticate(user=owner)

    response = api_client.delete(f"/api/tasks/{task.id}/")

    assert response.status_code == 403
    assert Task.objects.filter(id=task.id).exists()

@pytest.mark.django_db
def test_assigning_task_to_non_team_member_fails(api_client, owner, member, project):
    outsider = User.objects.create_user(username="outsider", email="outsider@example.com", password="pass12345")
    task = Task.objects.create(title="Task 1", project=project, created_by=owner)
    api_client.force_authenticate(user=owner)
    response = api_client.patch(f"/api/tasks/{task.id}/", {"assignee": outsider.id})
    assert response.status_code == 400

