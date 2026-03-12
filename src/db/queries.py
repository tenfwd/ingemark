import uuid

from typing import List
from uuid import UUID
from datetime import datetime
from asyncpg import Connection, Record

from src.models import MessageCreation, MessageUpdate


async def create_messages_query(
    conn: Connection,
    messages: List[MessageCreation],
) -> List[Record]:
    
    message_ids, chat_ids, contents, ratings, sent_ats, roles = [], [], [], [], [], []
    
    for message in messages:
        message_ids.append(uuid.uuid4())
        chat_ids.append(message.chat_id)
        contents.append(message.content)
        ratings.append(message.rating)
        sent_ats.append(datetime.now())
        roles.append(message.role)
    
    query = """
    INSERT INTO messages (message_id, chat_id, content, rating, sent_at, role)
    SELECT * FROM unnest($1::uuid[], $2::uuid[], $3::text[], $4::boolean[], $5::timestamp[], $6::text[])
    RETURNING *
    """
    return await conn.fetch(query, message_ids, chat_ids, contents, ratings, sent_ats, roles)


async def update_message_query(
    conn: Connection,
    message_id: UUID,
    message: MessageUpdate
) -> Record:
    updates, params, param_count = [], [], 1

    if message.content is not None:
        updates.append(f"content = ${param_count}")
        params.append(message.content)
        param_count += 1

    if message.rating is not None:
        updates.append(f"rating = ${param_count}")
        params.append(message.rating)
        param_count += 1

    if not updates:
        return None

    params.append(message_id)
    query = f"""
    UPDATE messages
    SET {', '.join(updates)}
    WHERE message_id = ${param_count}
    RETURNING *
    """
    return await conn.fetchrow(query, *params)


async def get_all_messages_query(conn: Connection) -> List[Record]:
    query = """
    SELECT * FROM messages
    ORDER BY sent_at DESC
    """
    return await conn.fetch(query)
