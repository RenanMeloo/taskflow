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