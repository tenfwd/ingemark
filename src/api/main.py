from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import DATABASE_URL
from src.api.routes import router
from src.db.client import asyncpg_client
from src.db.initialization import initialize_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncpg_client.connect(DATABASE_URL)
    await initialize_db(pool=asyncpg_client.pool)

    yield

    await asyncpg_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)
