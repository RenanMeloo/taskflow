import pytest


@pytest.mark.django_db
def test_user_can_update_own_profile(api_client, member):
    api_client.force_authenticate(user=member)

    response = api_client.patch(
        "/api/auth/profile/",
        {"first_name": "John", "last_name": "Doe", "username": "hacker"},
    )

    assert response.status_code == 200
    member.refresh_from_db()
    assert member.first_name == "John"
    assert member.last_name == "Doe"
    assert member.username == "member"


@pytest.mark.django_db
def test_user_can_register_and_login(api_client):
    credentials = {"username": "newuser", "password": "Str0ng-Pass-2026"}

    register_response = api_client.post(
        "/api/auth/register/",
        {**credentials, "email": "new@email.com"},
    )
    assert register_response.status_code == 201
    assert "password" not in register_response.data

    login_response = api_client.post("/api/auth/token/", credentials)
    assert login_response.status_code == 200
    assert "access" in login_response.data
