import atexit
import logging
from datetime import datetime
from typing import List

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from data_model.subscription_list import SubscriptionList
from services.caching_service import CachingService
from services.mysql_service import MySqlService
from services.weather_service import WeatherService
from utils.logger_utils import DIR_PATH


class EmailService:
    def __init__(
        self,
        caching_service: CachingService,
        mysql_service: MySqlService,
        weather_service: WeatherService,
        config,
    ):
        self.caching_service = caching_service
        self.mysql_service = mysql_service
        self.weather_service = weather_service
        self.config = config

    def run_mail_service(self) -> None:
        refresh_rate = int(
            self.config.get("EMAIL_SERVICE_REFRESH", 3600)
        )  # Default every hour
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func=self.collect_data_and_send_mail,
            trigger="interval",
            seconds=refresh_rate,
        )
        scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

    def collect_data_and_send_mail(self) -> None:
        open_weather_url = self.config.get("OPEN_WEATHER_MAP_HOST")
        open_weather_api_key = self.config.get("OPEN_WEATHER_MAP_KEY")

        all_subscriptions = self.get_active_subscriptions()

        # Get distinct location names of active locations
        locations = {
            loc.location: {"lat": loc.latitude, "lon": loc.longitude}
            for loc in all_subscriptions
        }

        # O(n*m) - Could do with optimising
        for loc, val in locations.items():
            lat = val["lat"]
            lon = val["lon"]

            # Only called for each unique location
            req = requests.get(
                f"{open_weather_url}2.5/weather?lat={lat}&lon={lon}&units=metric&appid={open_weather_api_key}"
            )

            if req.status_code != 200:
                logging.error(
                    f"Bad request to open weather map. Response code: {req.status_code}"
                )
                return

            wd = req.json()
            users_for_location = [u for u in all_subscriptions if u.location == loc]
            for user in users_for_location:

                ws = wd["wind"]["speed"]
                wc = wd["weather"][0]["id"]
                wt = wd["main"]["temp"]

                if ws > user.wind_speed_exceeds:
                    subject, mail_text = self.create_mail_text(
                        user,
                        "wind speed exceeds",
                        user.wind_speed_exceeds,
                        wd["wind"]["speed"],
                    )
                    self.send_mail(subject, mail_text, user.email, user.location)
                if wc == user.weather_code:
                    weather_str = self.weather_service.get_weather_for_code(
                        user.weather_code
                    )
                    subject, mail_text = self.create_mail_text(
                        user, "weather type equals", weather_str, weather_str
                    )
                    self.send_mail(subject, mail_text, user.email, user.location)
                if wt > user.temp_celsius_above:
                    subject, mail_text = self.create_mail_text(
                        user, "temperature exceeds", user.temp_celsius_above, wt
                    )
                    self.send_mail(subject, mail_text, user.email, user.location)
                if wt < user.temp_celsius_below:
                    subject, mail_text = self.create_mail_text(
                        user, "temperature falls below", user.temp_celsius_below, wt
                    )
                    self.send_mail(subject, mail_text, user.email, user.location)

    def send_mail(
        self, subject: str, mail_text: str, email: str, location: str
    ) -> None:
        now = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        with open(f"{DIR_PATH}/mock_emails/{email}-{location}_{now}.txt", "w") as f:
            f.write(f"{subject}\n\n")
            f.write(mail_text)

    def create_mail_text(
        self, user: SubscriptionList, metric: str, user_value, weather_value
    ) -> tuple[str, str]:
        subject = f"Weather Alert for {user.email} - {user.location}"
        mail_text = f"Your alert for {metric} {user_value} has been met. Value reported for {user.location} is {weather_value}."
        return subject, mail_text

    def get_active_subscriptions(self) -> List[SubscriptionList]:
        active_subscriptions = [
            SubscriptionList(a_s) for a_s in self.mysql_service.get_all_subscriptions()
        ]
        return active_subscriptions
