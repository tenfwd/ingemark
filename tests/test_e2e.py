import pytest
import httpx
import os
from uuid import uuid4

API_URL = os.getenv("API_URL", "http://localhost:8000")
AUTH_HEADER = {"Authorization": "Bearer test-token-123"}


@pytest.mark.asyncio
async def test_create_and_read_messages():
    async with httpx.AsyncClient(base_url=API_URL) as client:
        chat_id = str(uuid4())
        
        create_payload = [
            {
                "chat_id": chat_id,
                "content": "Test message from user",
                "role": "user",
                "rating": True
            },
            {
                "chat_id": chat_id,
                "content": "Test response from AI",
                "role": "ai",
                "rating": None
            }
        ]
        
        create_response = await client.post(
            "/messages/create",
            json=create_payload,
            headers=AUTH_HEADER
        )
        assert create_response.status_code == 200
        created_messages = create_response.json()
        assert len(created_messages) == 2
        assert created_messages[0]["content"] == "Test message from user"
        assert created_messages[0]["rating"] is True
        assert created_messages[1]["content"] == "Test response from AI"
        assert created_messages[1]["rating"] is None
        
        get_response = await client.get("/messages", headers=AUTH_HEADER)
        assert get_response.status_code == 200
        all_messages = get_response.json()
        assert len(all_messages) >= 2
        
        message_ids = [msg["message_id"] for msg in created_messages]
        fetched_ids = [msg["message_id"] for msg in all_messages]
        assert all(msg_id in fetched_ids for msg_id in message_ids)


@pytest.mark.asyncio
async def test_update_message():
    async with httpx.AsyncClient(base_url=API_URL) as client:
        chat_id = str(uuid4())
        
        create_payload = [
            {
                "chat_id": chat_id,
                "content": "Original content",
                "role": "user",
                "rating": None
            }
        ]
        
        create_response = await client.post(
            "/messages/create",
            json=create_payload,
            headers=AUTH_HEADER
        )
        assert create_response.status_code == 200
        created_message = create_response.json()[0]
        message_id = created_message["message_id"]
        
        update_payload = {
            "content": "Updated content",
            "rating": True
        }
        
        update_response = await client.put(
            f"/messages/{message_id}",
            json=update_payload,
            headers=AUTH_HEADER
        )
        assert update_response.status_code == 200
        updated_message = update_response.json()
        assert updated_message["content"] == "Updated content"
        assert updated_message["rating"] is True
        assert updated_message["message_id"] == message_id
        
        get_response = await client.get("/messages", headers=AUTH_HEADER)
        assert get_response.status_code == 200
        all_messages = get_response.json()
        updated_in_list = next(
            (msg for msg in all_messages if msg["message_id"] == message_id),
            None
        )
        assert updated_in_list is not None
        assert updated_in_list["content"] == "Updated content"
        assert updated_in_list["rating"] is True


@pytest.mark.asyncio
async def test_authentication_required():
    async with httpx.AsyncClient(base_url=API_URL) as client:
        response = await client.get("/messages")
        assert response.status_code == 401
        assert "authorization" in response.json()["detail"].lower()
        
        response = await client.get(
            "/messages",
            headers={"Authorization": "InvalidFormat"}
        )
        assert response.status_code == 401
