import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Railway автоматически передает этот env-переменную

async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

db_pool = None

async def init_db():
    global db_pool
    db_pool = await create_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY,
                name TEXT NOT NULL,
                username TEXT
            )
        """)

async def add_user(user_id: int, name: str, username: str):
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (id, name, username) 
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
        """, user_id, name, username)

async def get_users():
    async with db_pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM users")
