import logging
import pickle
import zlib
from threading import Lock

import redis

from utils.utils import DEFAULT_CACHE_TIMEOUT

LOG = logging.getLogger(__name__)

CACHE_KEY_WEATHER_CODES = "CACHE_KEY_WEATHER_CODES"


class CachingService:
    def __init__(self, config):
        self.config = config
        self.lock = Lock()

        self.redis_host = self.config.get("REDIS_HOST")
        self.redis_port = self.config.get("REDIS_PORT", 6379)

        if self.redis_host is None:
            LOG.warning("No redis cache specified, assuming no cache")
            self.redis = None
        else:
            try:
                LOG.debug(f"Initialising Redis for {self.redis_host}")
                self.redis = redis.Redis(
                    host=self.redis_host, port=int(self.redis_port)
                )

            except Exception as e:
                LOG.error(f"Problem initialising redis, assuming no cache: {e}")

    def info(self):
        if self.redis is None:
            return {}
        try:
            return self.redis.info()
        except Exception as e:
            LOG.error(f"Problem getting redis info: {e}")
        return {}

    def get(self, key):
        if self.redis is None:
            return None
        try:
            with self.lock:
                value = self.redis.get(key)
                if value is None:
                    LOG.debug(f"CACHE MISS: {key}")
                    return None
                return pickle.loads(zlib.decompress(value))
        except Exception as e:
            LOG.exception(f"Problem initialising redis, assuming no cache: {e}")
            return None

    def put(self, key, value, ex_seconds=DEFAULT_CACHE_TIMEOUT) -> None:
        if self.redis is None:
            return
        try:
            with self.lock:
                dumps = zlib.compress(pickle.dumps(value))
                self.redis.set(key, dumps, ex_seconds)
        except Exception as e:
            LOG.exception(f"Problem reading redis, assuming no cache: {e}")
