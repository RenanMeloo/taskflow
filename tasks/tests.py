import pytest

from tasks.models import Task
from users.models import User


@pytest.mark.django_db
def test_member_can_create_task(api_client, member, project):
    api_client.force_authenticate(user=member)
    response = api_client.post(
        "/api/tasks/",
        {"title": "Task 1", "description": "Test task", "project": project.id},
    )
    assert response.status_code == 201
    task = Task.objects.get(title="Task 1")
    assert task.created_by == member


@pytest.mark.django_db
def test_outsider_cannot_see_task(api_client, project):
    # create a task in the project and an outsider user
    task = Task.objects.create(
        title="task 1",
        description="test task",
        project=project,
        created_by=project.team.owner,
    )
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


@pytest.mark.django_db
def test_member_can_comment_on_task(api_client, member, project):
    task = Task.objects.create(title="Task 1", project=project, created_by=member)
    api_client.force_authenticate(user=member)
    response = api_client.post(f"/api/tasks/{task.id}/comments/", {"content": "This is a comment"})
    assert response.status_code == 201
    assert response.data["content"] == "This is a comment"
    assert response.data["author"] == member.id


@pytest.mark.django_db
def test_filter_tasks_by_status(api_client, member, project):
    Task.objects.create(title="Pending task", project=project, status=Task.Status.TODO)
    Task.objects.create(title="Finished task", project=project, status=Task.Status.DONE)
    api_client.force_authenticate(user=member)

    response = api_client.get("/api/tasks/?status=done")

    assert response.status_code == 200
    titles = [task["title"] for task in response.data["results"]]
    assert titles == ["Finished task"]

@pytest.mark.django_db
def test_order_tasks_by_priority_level(api_client, member, project):
    Task.objects.create(title="Low priority task", project=project, priority=Task.Priority.LOW)
    Task.objects.create(title="High priority task", project=project, priority=Task.Priority.HIGH)
    Task.objects.create(title="Medium priority task", project=project, priority=Task.Priority.MEDIUM)
    api_client.force_authenticate(user=member)

    response = api_client.get("/api/tasks/?ordering=priority_level")

    assert response.status_code == 200
    titles = [task["title"] for task in response.data["results"]]
    assert titles == ["Low priority task", "Medium priority task", "High priority task"]

@pytest.mark.django_db
def test_member_cannot_delete_orphan_task(api_client, member, project):
    # The creator is no longer part of the team, so the task is orphaned
    outsider = User.objects.create_user(username="outsider", email="outsider@test.com", password="pass12345")
    task = Task.objects.create(title="Orphan task", project=project, created_by=outsider)
    api_client.force_authenticate(user=member)

    response = api_client.delete(f"/api/tasks/{task.id}/")

    assert response.status_code == 403
    assert Task.objects.filter(id=task.id).exists()

@pytest.mark.django_db
def test_admin_can_delete_orphan_task(api_client, admin, project):
    # The creator is no longer part of the team, so the task is orphaned
    outsider = User.objects.create_user(username="outsider", email="outsider@test.com", password="pass12345")
    task = Task.objects.create(title="Orphan task", project=project, created_by=outsider)
    api_client.force_authenticate(user=admin)

    response = api_client.delete(f"/api/tasks/{task.id}/")

    assert response.status_code == 204
    assert not Task.objects.filter(id=task.id).exists()