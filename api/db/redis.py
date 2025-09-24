import redis.asyncio as aio_redis
import json
from typing import Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()


# Redis client for asynchronous operations
class RedisClient:
    def __init__(
        self,
        host: str = os.getenv("REDIS_HOST"),
        port: int = os.getenv("REDIS_PORT"),
        db: int = 0,
        password: str = os.getenv("REDIS_PASSWORD"),
        decode_responses: bool = True,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.connection: Optional[aio_redis.Redis] = None

    # Connect to Redis
    async def connect(self):
        if not self.connection:
            try:
                self.connection = aio_redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    password=self.password,
                    decode_responses=self.decode_responses,
                )
                await self.connection.ping()
            except Exception as e:
                raise ConnectionError(f"Failed to connect to Redis: {e}")
        return self.connection

    # Disconnect from Redis
    async def disconnect(self):
        if self.connection:
            await self.connection.aclose()
            self.connection = None

    # Get a value by key
    async def get(self, key: str) -> Any:
        try:
            redis = await self.connect()
            return await redis.get(key)
        except Exception as e:
            print(f"Error getting key from Redis: {e}")
            return None

    # Set a value by key with optional expiration
    async def set(self, key: str, value: Any, ex: int = None) -> bool:
        redis = await self.connect()
        return await redis.set(key, value, ex=ex)

    # Delete a key
    async def delete(self, key: str) -> Any | None:
        try:
            redis = await self.connect()
            return await redis.delete(key)
        except Exception as e:
            print(f"Error deleting key from Redis: {e}")

    # Cache JSON data with a TTL (time to live)
    async def cache_json(self, key: str, data: dict, ttl: int = 300):
        try:
            redis = await self.connect()
            await redis.set(key, json.dumps(data), ex=ttl)
        except Exception as e:
            print(f"Error caching JSON to Redis: {e}")

    # Retrieve JSON data by key
    async def get_json(self, key: str) -> Optional[dict]:
        try:
            redis = await self.connect()
            data = await redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Error retrieving JSON from Redis: {e}")
            return None


# Singleton instance of RedisClient
redis_client = RedisClient()
