import pytest
from fastapi.testclient import TestClient
from helpers import assertions, crud
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("test_db")
def test_health_check(client: TestClient) -> None:
    response = client.get("/health-check")

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.usefixtures("test_db")
def test_unauthorized(client: TestClient) -> None:
    dummy_id = 99999

    response = client.get("/users/")
    assert response.status_code == 401, response.text

    response = client.get(f"/users/{dummy_id}")
    assert response.status_code == 401, response.text

    response = client.post(
        f"/users/{dummy_id}/items",
        json={
            "title": "Test Item",
            "description": "This is test item",
        },
    )
    assert response.status_code == 401, response.text

    response = client.get("/items")
    assert response.status_code == 401, response.text


@pytest.mark.usefixtures("test_db")
def test_happy_path(client: TestClient, db_session: Session) -> None:
    # 1. create user
    email1 = "deadpool@example.com"
    user_id1, token1 = assertions.user.post(client, email1, "chimichangas4life")
    assertions.user.get(client, user_id1, email1, token1)

    email2 = "wade-winston-wilson@example.com"
    user_id2, token2 = assertions.user.post(client, email2, "preferTacos2chimichangas")
    assertions.user.get(client, user_id2, email2, token2)

    email3 = "ryan-rodney-reynolds@example.com"
    user_id3, token3 = assertions.user.post(client, email3, "iLoveGuns")
    assertions.user.get(client, user_id3, email3, token3)

    assertions.item.get(client, token1, [])

    # prepare expected items
    prepared_items = []

    expected_item1 = {
        "title": "First Item",
        "description": "This is first item",
        "created_at": "2023-01-01T00:00:00",
        "owner_id": user_id1,
        "done": False,
    }
    prepared_items.append((expected_item1, token1))

    expected_item2 = {
        "title": "Second Item",
        "description": "This is second item",
        "created_at": "2023-01-02T00:00:00",
        "owner_id": user_id1,
        "done": False,
    }
    prepared_items.append((expected_item2, token1))

    expected_item3 = {
        "title": "Third Item",
        "description": "This is third item",
        "created_at": "2023-01-03T00:00:00",
        "owner_id": user_id1,
        "done": True,
    }
    prepared_items.append((expected_item3, token1))

    expected_item4 = {
        "title": "Fourth Item",
        "description": "This is fourth item",
        "created_at": "2022-12-31T00:00:00",
        "owner_id": user_id2,
        "done": True,
    }
    prepared_items.append((expected_item4, token2))

    expected_item5 = {
        "title": "Fifth Item",
        "description": "This is fifth item",
        "created_at": "2023-01-03T12:00:00",
        "owner_id": user_id2,
        "done": False,
    }
    prepared_items.append((expected_item5, token2))

    expected_item6 = {
        "title": "Sixth Item",
        "description": "This is sixth item",
        "created_at": "2023-01-04T00:00:00",
        "owner_id": user_id3,
        "done": False,
    }
    prepared_items.append((expected_item6, token3))

    for prepared_item, token in prepared_items:
        item_id = assertions.item.post(
            client,
            prepared_item["owner_id"],
            token,
            prepared_item["title"],
            prepared_item["description"],
        )
        prepared_item["id"] = item_id

        crud.item.update_created_at(db_session, item_id, prepared_item["created_at"])

        if prepared_item["done"]:
            assertions.item.patch(
                client,
                prepared_item["owner_id"],
                token,
                item_id,
                prepared_item["title"],
                prepared_item["description"],
                prepared_item["done"],
            )

    # 2. get items
    ordered_full_items = [
        expected_item6,
        expected_item5,
        expected_item3,
        expected_item2,
        expected_item1,
        expected_item4,
    ]
    assertions.item.get(client, token1, ordered_full_items)
    assertions.item.get(
        client,
        token1,
        [expected_item6, expected_item5, expected_item2, expected_item1],
        done=False,
    )
    assertions.item.get(client, token1, [expected_item3, expected_item4], done=True)
    assertions.item.get(
        client, token1, [expected_item5, expected_item3], date="20230103"
    )
    assertions.item.get(client, token1, [expected_item3], date="20230103", done=True)

    # 3. delete user
    assertions.user.delete(client, user_id2, token1)
    expected_item4["owner_id"] = user_id1
    expected_item5["owner_id"] = user_id1
    assertions.item.get(client, token1, ordered_full_items)

    assertions.user.delete(client, user_id1, token3)
    expected_item1["owner_id"] = user_id3
    expected_item2["owner_id"] = user_id3
    expected_item3["owner_id"] = user_id3
    expected_item4["owner_id"] = user_id3
    expected_item5["owner_id"] = user_id3
    assertions.item.get(client, token3, ordered_full_items)
