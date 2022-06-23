import logging
import pickle
import zlib
from threading import Lock

import redis

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
            self.r = None

        else:
            try:
                LOG.debug(f"Initialising Redis for {self.redis_host}")
                self.r = redis.Redis(host=self.redis_host, port=int(self.redis_port))

            except Exception as e:
                LOG.error(f"Problem initialising redis, assuming no cache: {e}")

    def info(self):
        if self.r is None:
            return {}

        try:
            return self.r.info()
        except Exception as e:
            LOG.error(f"Problem getting redis info: {e}")
        return {}

    def get(self, key):
        if self.r is None:
            return None

        try:
            with self.lock:
                v = self.r.get(key)
                if v is None:
                    LOG.debug(f"CACHE MISS: {key}")
                    return None
                return pickle.loads(zlib.decompress(v))
        except Exception as e:
            LOG.exception(f"Problem initialising redis, assuming no cache: {e}")
            return None

    def put(self, key, value, ex_seconds=10800):  # 3 Hours
        if self.r is None:
            return
        try:
            with self.lock:
                d = zlib.compress(pickle.dumps(value))
                self.r.set(key, d, ex_seconds)
        except Exception as e:
            LOG.exception(f"Problem reading redis, assuming no cache: {e}")
