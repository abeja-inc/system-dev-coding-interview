from typing import Dict, List, Optional, TypedDict

from fastapi.testclient import TestClient


class _ExpectedItem(TypedDict):
    title: str
    description: str
    created_at: str
    id: str
    owner_id: str
    done: bool


def post(
    client: TestClient,
    user_id: str,
    token: str,
    title: str,
    description: str,
) -> str:
    """assert post item

    Args:
        client: test client
        user_id: id of user
        token: token of user
        title: title of item
        description: description of item
        created_at: created_at of item(format is %Y-%m-%dT%H:%M:%S)

    Returns:
        id of created item
    """
    response = client.post(
        f"/users/{user_id}/items",
        headers={"X-API-TOKEN": token},
        json={"title": title, "description": description},
    )

    assert response.status_code == 200, response.text
    data = response.json()

    assert "id" in data
    assert "created_at" in data
    assert data["title"] == title
    assert data["description"] == description
    assert data["owner_id"] == user_id
    assert not data["done"]

    return data["id"]


def patch(
    client: TestClient,
    user_id: str,
    token: str,
    item_id: str,
    title: str,
    description: str,
    done: bool,
) -> None:
    """assert patch item

    Args:
        client: test client
        user_id: id of user
        token: token of user
        item_id: id of item
        title: title of item
        description: description of item
        done: done of item
    """
    response = client.patch(
        f"/users/{user_id}/items/{item_id}",
        headers={"X-API-TOKEN": token},
        json={"title": title, "description": description, "done": done},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["id"] == item_id
    assert data["title"] == title
    assert data["description"] == description
    assert data["owner_id"] == user_id
    assert data["done"] == done


def get(
    client: TestClient,
    token: str,
    expected: List[_ExpectedItem],
    date: Optional[str] = None,
    done: Optional[bool] = None,
) -> None:
    """assert get items

    Args:
        client: test client
        token: token of user
        expected: expected items
        date: date to filter
        done: done to filter
    """
    params: Dict[str, str] = {}
    if date is not None:
        params["date"] = date
    if done is not None:
        params["done"] = str(done)

    response = client.get(
        "/items",
        headers={"X-API-TOKEN": token},
        params=params,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data == expected
