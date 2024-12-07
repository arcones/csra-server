import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post("/items/", json={"name": "Test Item", "description": "A test item"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"


@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    response = await client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient):
    # Create a test item first
    create_response = await client.post("/items/", json={"name": "Test Item", "description": "A test item"})
    item_id = create_response.json()["id"]

    # Fetch the item
    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient):
    # Create a test item first
    create_response = await client.post("/items/", json={"name": "Test Item", "description": "A test item"})
    item_id = create_response.json()["id"]

    # Update the item
    response = await client.put(f"/items/{item_id}", json={"name": "Updated Item", "description": "Updated description"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    # Create a test item first
    create_response = await client.post("/items/", json={"name": "Test Item", "description": "A test item"})
    item_id = create_response.json()["id"]

    # Delete the item
    response = await client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted"
