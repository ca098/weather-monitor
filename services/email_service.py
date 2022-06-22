import time
import atexit
import requests

from apscheduler.schedulers.background import BackgroundScheduler

from data_model.subscription_list import SubscriptionList
from services.caching_service import CachingService
from services.mysql_service import MySqlService


class EmailService:
    def __init__(self, caching_service: CachingService, mysql_service: MySqlService, config: dict):
        self.caching_service = caching_service
        self.mysql_service = mysql_service
        self.config = config

    def run_mail_service(self):
        refresh_rate = int(self.config.get("EMAIL_SERVICE_REFRESH", 3600))

        self.send_mail()

        scheduler = BackgroundScheduler()
        scheduler.add_job(func=print_date_time, trigger="interval", seconds=refresh_rate)
        scheduler.start()

        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

    def send_mail(self):
        open_weather_url = self.config.get("OPEN_WEATHER_MAP_HOST")
        open_weather_api_key = self.config.get("OPEN_WEATHER_MAP_KEY")

        "https://api.openweathermap.org/data/"
        all_subscriptions = self.get_active_subscriptions()

        # Get distinct location names
        locations = {loc.location: [{"lat": loc.latitude, "lon": loc.longitude}] for loc in all_subscriptions}

        # TODO - Tests, optimise this method & README.md

        for loc in locations:
            pass

    def get_active_subscriptions(self):
        all_subscriptions = [SubscriptionList(a_s) for a_s in self.mysql_service.get_all_subscriptions()]
        return all_subscriptions


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
