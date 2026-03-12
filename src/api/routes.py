from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection
from typing import List, Dict
from src.db.queries import create_messages_query, get_all_messages_query, update_message_query
from src.models import MessageCreation, MessageResponse, MessageUpdate
from src.dependencies import get_db_connection, authenticate_user
from src.logging import get_logger

logger = get_logger(__name__)


router = APIRouter()


@router.post("/messages/create")
async def create_messages(
    messages: List[MessageCreation],
    conn: Connection = Depends(get_db_connection),
    _: Dict = Depends(authenticate_user)
) -> List[MessageResponse]:
    try:
        response = await create_messages_query(conn=conn, messages=messages)
        return [MessageResponse(**dict(record)) for record in response]
    except Exception as e:
        logger.error(f"Error creating messages: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/messages/{message_id}")
async def update_message(
    message_id: UUID,
    message: MessageUpdate,
    conn: Connection = Depends(get_db_connection),
    _: Dict = Depends(authenticate_user)
) -> MessageResponse:
    try:
        response = await update_message_query(conn=conn, message_id=message_id, message=message)
        return MessageResponse(**dict(response))
    except Exception as e:
        logger.error(f"Error updating message {message_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/messages")
async def get_messages(
    conn: Connection = Depends(get_db_connection),
    _: Dict = Depends(authenticate_user)
) -> List[MessageResponse]:
    try:
        response = await get_all_messages_query(conn=conn)
        return [MessageResponse(**dict(record)) for record in response]
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
