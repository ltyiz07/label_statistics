import os
import redis

cache = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"))


def test_redis_connection():
    key = "test"
    value = "test value"
    cache.set(key, value)
    assert cache.get(key).decode() == value


def test_redis_set():
    key = "set test"
    values = ['first', 'second', 'third']
    cache.sadd(key, values[0])
    cache.sadd(key, values[1])
    cache.sadd(key, values[2])
    assert values[0].encode() in cache.smembers(key)
    assert values[1].encode() in cache.smembers(key)
    assert values[2].encode() in cache.smembers(key)
