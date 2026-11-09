import pytest

from users.models import User

from .models import Membership, Team


@pytest.mark.django_db
def test_creator_becomes_owner(api_client, owner):
    api_client.force_authenticate(user=owner)
    response = api_client.post("/api/teams/", {"name": "Backend"})
    assert response.status_code == 201
    team_id = response.data["id"]
    assert Membership.objects.filter(user=owner, team_id=team_id, role=Membership.Role.OWNER).exists()


@pytest.mark.django_db
def test_member_cannot_edit_team(api_client, member, team):
    api_client.force_authenticate(user=member)

    response = api_client.patch(f"/api/teams/{team.id}/", {"name": "Frontend"})

    assert response.status_code == 403
    team.refresh_from_db()
    assert team.name == "Backend"


@pytest.mark.django_db
def test_admin_can_edit_team(api_client, admin, team):
    api_client.force_authenticate(user=admin)

    response = api_client.patch(f"/api/teams/{team.id}/", {"name": "Frontend"})

    assert response.status_code == 200
    team.refresh_from_db()
    assert team.name == "Frontend"


@pytest.mark.django_db
def test_admin_cannot_delete_team(api_client, admin, team):
    api_client.force_authenticate(user=admin)

    response = api_client.delete(f"/api/teams/{team.id}/")

    assert response.status_code == 403
    assert Team.objects.filter(id=team.id).exists()


@pytest.mark.django_db
def test_owner_role_cannot_be_assigned(api_client, owner, team):
    new_user = User.objects.create_user(username="newuser", email="new@test.com", password="pass12345")
    api_client.force_authenticate(user=owner)

    response = api_client.post(
        f"/api/teams/{team.id}/members/",
        {"user": new_user.id, "role": Membership.Role.OWNER},
    )

    assert response.status_code == 400
    assert not Membership.objects.filter(user=new_user, team=team).exists()


@pytest.mark.django_db
def test_cannot_add_duplicate_member(api_client, owner, member, team):
    api_client.force_authenticate(user=owner)

    response = api_client.post(
        f"/api/teams/{team.id}/members/",
        {"user": member.id, "role": Membership.Role.MEMBER},
    )

    assert response.status_code == 400
    assert Membership.objects.filter(user=member, team=team).count() == 1


@pytest.mark.django_db
def test_owner_cannot_be_removed(api_client, owner, team):
    api_client.force_authenticate(user=owner)

    response = api_client.delete(f"/api/teams/{team.id}/members/{owner.id}/")

    assert response.status_code == 400
    assert Membership.objects.filter(user=owner, team=team).exists()


@pytest.mark.django_db
def test_admin_cannot_remove_owner(api_client, owner, admin, team):
    api_client.force_authenticate(user=admin)

    response = api_client.delete(f"/api/teams/{team.id}/members/{owner.id}/")

    assert response.status_code == 400
    assert Membership.objects.filter(user=owner, team=team).exists()


@pytest.mark.django_db
def test_outsider_cannot_see_team(api_client, team):
    outsider = User.objects.create_user(username="outsider", email="outsider@test.com", password="pass12345")
    api_client.force_authenticate(user=outsider)
    response = api_client.get(f"/api/teams/{team.id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_admin_can_remove_member(api_client, admin, member, team):
    api_client.force_authenticate(user=admin)

    response = api_client.delete(f"/api/teams/{team.id}/members/{member.id}/")

    assert response.status_code == 204
    assert not Membership.objects.filter(user=member, team=team).exists()
