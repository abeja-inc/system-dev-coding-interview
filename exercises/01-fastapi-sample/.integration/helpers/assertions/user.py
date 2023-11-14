from typing import Tuple

from fastapi.testclient import TestClient


def post(client: TestClient, email: str, password: str) -> Tuple[str, str]:
    """assert post user

    Args:
        client: test client
        email: email of user
        password: password of user

    Returns:
        id and token of created user
    """
    response = client.post(
        "/users",
        json={"email": email, "password": password},
    )

    assert response.status_code == 200, response.text
    data = response.json()

    assert "id" in data
    assert data["email"] == email
    return data["id"], data["token"]


def get(client: TestClient, user_id: str, email: str, token: str) -> None:
    """assert get user

    Args:
        client: test client
        user_id: id of user
        email: email of user
        token: token of user
    """
    response = client.get(
        f"/users/{user_id}",
        headers={"X-API-TOKEN": token},
    )

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == email


def delete(client: TestClient, user_id: str, token: str) -> None:
    """assert delete user

    Args:
        client: test client
        user_id: id of user
        token: token of user
    """
    response = client.delete(
        f"/users/{user_id}",
        headers={"X-API-TOKEN": token},
    )
    assert response.status_code == 200, response.text

    response = client.get(
        f"/users/{user_id}",
        headers={"X-API-TOKEN": token},
    )
    assert response.status_code == 404, response.text
