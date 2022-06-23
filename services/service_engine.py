import os

from services.caching_service import CachingService
from services.email_service import EmailService
from services.mysql_service import MySqlService
from services.weather_service import WeatherService


class ServiceEngine(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceEngine, cls).__new__(cls)
            cls._instance.config = os.environ
            cls._instance.mysql_service = MySqlService(cls._instance.config)
            cls._instance.caching_service = CachingService(cls._instance.config)
            cls._instance.weather_service = WeatherService(
                cls._instance.caching_service,
                cls._instance.mysql_service,
                cls._instance.config,
            )
            cls._instance.email_service = EmailService(
                cls._instance.caching_service,
                cls._instance.mysql_service,
                cls._instance.weather_service,
                cls._instance.config,
            )

        return cls._instance
