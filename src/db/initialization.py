CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    message_id UUID PRIMARY KEY,
    chat_id UUID NOT NULL,
    content TEXT NOT NULL,
    rating BOOLEAN,
    sent_at TIMESTAMP NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('ai', 'user'))
);
"""


async def initialize_db(pool):
    async with pool.acquire() as conn:
        await conn.execute(CREATE_MESSAGES_TABLE)
