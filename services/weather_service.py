import logging
import re
from typing import Optional

import requests

from data_model.location import Location
from data_model.subscription import Subscription
from data_model.subscription_list import SubscriptionList
from data_model.weather_codes import WeatherCodes
from services.caching_service import CACHE_KEY_WEATHER_CODES, CachingService
from services.mysql_service import MySqlService
from utils.utils import SUBSCRIPTION_DEFAULTS, StatusCode

LOG = logging.getLogger(__name__)


class WeatherService:
    def __init__(
        self, caching_service: CachingService, mysql_service: MySqlService, config
    ):
        self.caching_service = caching_service
        self.mysql_service = mysql_service
        self.config = config

        self.open_cage_base_url = self.config.get("OPEN_CAGE_DATA_URL")
        self.open_cage_data_key = self.config.get("OPEN_CAGE_DATA_KEY")

    def create_new_subscription(self, email: str, location: str, params: dict) -> dict:
        defaults = SUBSCRIPTION_DEFAULTS
        defaults.update(params)

        lat_lon = self.get_latitude_and_longitude(location)
        if not lat_lon:
            return {
                "error": f"The location '{location}' was not found. Make sure it was entered correctly."
            }

        loc_id = lat_lon["id"]
        existing_record = next(
            (
                Subscription(s)
                for s in self.mysql_service.get_subscription(
                    email=email, location_id=loc_id
                )
            ),
            None,
        )

        # Return if pre-existing record (could be changed to call update record?)
        if existing_record:
            return {
                "error": f"Entry already exists for the email '{email}', and location '{location}'."
                f" Please remove the entry to be able to add a new one."
            }

        sub_rec_id = self.mysql_service.insert_subscription(
            email=email, location_id=loc_id
        )
        self.mysql_service.insert_subscribed_metric(
            subscription_id=sub_rec_id,
            temp_celsius_above=defaults["tempCelsiusAbove"],
            temp_celsius_below=defaults["tempCelsiusBelow"],
            weather_code=defaults["weatherCodeEquals"],
            wind_speed_exceeds=defaults["windSpeedExceeds"],
        )

        return {"message": f"Subscription has been created successfully"}

    def update_subscription(self, email: str, location: str, params: dict) -> dict:
        defaults = SUBSCRIPTION_DEFAULTS
        defaults.update(params)

        lat_lon = self.get_latitude_and_longitude(location)
        if not lat_lon:
            return {
                "error": f"The location '{location}' was not found. Make sure it was entered correctly."
            }

        loc_id = lat_lon["id"]
        subscriptions = (
            Subscription(s)
            for s in self.mysql_service.get_subscription(
                email=email, location_id=loc_id
            )
        )
        existing_record = next(subscriptions, None)
        if existing_record:
            self.mysql_service.update_subscription(
                existing_record.id,
                temp_celsius_above=defaults["tempCelsiusAbove"],
                temp_celsius_below=defaults["tempCelsiusBelow"],
                weather_code=defaults["weatherCodeEquals"],
                wind_speed_exceeds=defaults["windSpeedExceeds"],
            )

            return {"message": f"Subscription has been updated successfully"}

        else:
            return {
                "error": f"No subscription found for the location '{location}', and email '{email}'."
            }

    def delete_subscription(self, email: str, location: str) -> dict:
        lat_lon = self.get_latitude_and_longitude(location)
        if not lat_lon:
            return {
                "error": f"The location '{location}' was not found. Make sure it was entered correctly."
            }
        loc_id = lat_lon["id"]
        subscriptions = (
            Subscription(s)
            for s in self.mysql_service.get_subscription(
                email=email, location_id=loc_id
            )
        )
        existing_record = next(subscriptions, None)
        if existing_record:
            self.mysql_service.delete_subscription(existing_record.id)
            return {
                "message": f"Subscription for email '{email}' and location '{location}' has been removed."
            }
        else:
            return {
                "error": f"Subscription for email '{email}' and location '{location}' was not found."
            }

    def get_subscription_list(self, email: str) -> [dict]:
        subscriptions = [
            SubscriptionList(es).to_digest_dict()
            for es in self.mysql_service.get_subscriptions_by_email(email)
        ]
        return subscriptions

    def get_weather_for_code(self, weather_code: int) -> Optional[str]:
        weather_codes = self.get_weather_codes()
        return next(
            (
                weather
                for weather, code in weather_codes.items()
                if int(code) == weather_code
            ),
            None,
        )

    def get_weather_codes(self) -> dict:
        cache_key = CACHE_KEY_WEATHER_CODES
        cached_result = self.caching_service.get(cache_key)
        if cached_result is not None:
            return cached_result

        weather_codes_list = self.mysql_service.get_weather_codes()
        if not weather_codes_list:
            return {}

        weather_codes = (
            WeatherCodes(weather_codes_list).to_digest_dict()
            if weather_codes_list
            else {}
        )
        self.caching_service.put(cache_key, weather_codes)
        return weather_codes

    def get_latitude_and_longitude(self, location: str) -> dict:
        if not re.match("^[A-Za-z0-9_-]*$", location):
            return {}
        try:
            location_cache_key = f"location_{location}"
            cached_location_value = self.caching_service.get(location_cache_key)
            if cached_location_value is not None:
                return cached_location_value

            # Fetch from DB
            stored_location = self.mysql_service.get_location_by_name(location=location)
            if stored_location:
                return next(
                    (Location(loc).to_digest_dict() for loc in stored_location), {}
                )

            open_cage_url = (
                f"{self.open_cage_base_url}q={location}&key={self.open_cage_data_key}"
            )
            open_cage_request = requests.get(open_cage_url)
            open_cage_data = open_cage_request.json()
            if (
                open_cage_request.status_code == StatusCode.OKAY
                and len(open_cage_data["results"]) > 0
            ):
                lat_lon = open_cage_data["results"][0]["geometry"]
                lat_lon["lat"] = format(lat_lon["lat"], ".2f")
                lat_lon["lng"] = format(lat_lon["lng"], ".2f")
                location_id = self.mysql_service.insert_location(
                    latitude=lat_lon["lat"], longitude=lat_lon["lng"], location=location
                )
                lat_lon["id"] = location_id

                self.caching_service.put(
                    location_cache_key, lat_lon, ex_seconds=43200
                )  # 12 Hours
                return lat_lon

            else:
                # Location not valid
                return {}
        except ConnectionError as e:
            LOG.error(f"Error connecting to OpenCage: {e}")
