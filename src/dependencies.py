from fastapi import Header, HTTPException
from src.db.client import asyncpg_client
from typing import Dict


async def get_db_connection():
    async with asyncpg_client.pool.acquire() as conn:
        yield conn

async def authenticate_user(authorization: str = Header(None)) -> Dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    # Simuliramo slanje nekakvog Auth tokena koji bi ovdje provjeravali. Za potrebe testiranja možemo poslati bilo kakav, samo da nije prazan.
    token = authorization.replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    
    return {"user_id": token}