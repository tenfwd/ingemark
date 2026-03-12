from src.logging import get_logger
import asyncpg
from typing import Optional

_PG_POOL_SIZE = 10

logger = get_logger(__name__)


class AsyncPGClient:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self, dsn: str, timeout: int = 10) -> None:
        if self.pool is None:
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=dsn,
                    min_size=2,
                    max_size=_PG_POOL_SIZE,
                    timeout=timeout,
                    command_timeout=timeout
                )
            except Exception as e:
                logger.error(f"Error creating pool: {e}")
                raise

    async def close(self) -> None:
        if self.pool:
            try:
                await self.pool.close()
            except Exception as e:
                logger.error(f"Error closing pool: {e}")
            finally:
                self.pool = None


asyncpg_client = AsyncPGClient()