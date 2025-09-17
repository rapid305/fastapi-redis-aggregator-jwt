import logging
import pytest

from api.db.redis import redis_client


@pytest.mark.asyncio
async def test_redis():
    await redis_client.connect()
    logging.log(logging.INFO, "Connected to Redis")

    await redis_client.set("test_key", "test_value", ex=10)
    logging.log(logging.INFO, "Set test_key in Redis")

    value = await redis_client.get("test_key")
    assert value == "test_value"

    await redis_client.delete("test_key")
    value = await redis_client.get("test_key")
    assert value is None

    await redis_client.disconnect()
    logging.log(logging.INFO, "Disconnected from Redis")
