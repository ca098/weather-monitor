import logging
import time
from threading import Lock
from typing import List, Optional

import mysql.connector as mysql

from db.queries import *

LOG = logging.getLogger(__name__)

WRITE_MODE = 'WRITE_MODE'
READ_MODE = 'READ_MODE'


class MySqlService:
    def __init__(self, config):
        self.config = config
        self.lock = Lock()
        self.host = self.config.get('DB_HOST')
        self.user = self.config.get('DB_USERNAME')
        self.passwd = self.config.get('DB_PASSWORD')
        self.database = self.config.get('DB_NAME')

        self.__connect__()

    def __connect__(self):
        try:
            cnx = self.__mysql_connect__()
        except Exception as e:
            logging.info(f'Connection to DB initially failed, restarting in 30 seconds: {str(e)}')
            time.sleep(30)
            cnx = self.__mysql_connect__()

        if cnx is not None and cnx.is_connected():
            return cnx

        LOG.warning("Warning: Failed to connect to the Database. Retrying...")
        time.sleep(30)
        cnx = self.__mysql_connect__()
        if cnx is None or not cnx.is_connected():
            LOG.error("Failed to get connection to database.")

    def __mysql_connect__(self):
        port = 3306
        try:
            return mysql.connect(host=self.host, user=self.user, passwd=self.passwd, port=port)
        except Exception as e:
            LOG.error('Connecting to the database failed, retrying in 15 seconds. \n\nERROR: ' + str(e))
            time.sleep(15)
            return mysql.connect(host=self.host, user=self.user, passwd=self.passwd, port=port)

    def __read__(self, query, params=None) -> List:
        try:
            db = self.__mysql_connect__()
            cursor = db.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            db.close()
            return results
        except Exception as e:
            LOG.error('Reading from database threw exception. Query: {}, Exception: {}'.format(query, str(e)))
            return []

    def __insert__(self, table: str, item_dict: dict) -> int:
        db = self.__mysql_connect__()
        id = 0
        try:
            cursor = db.cursor()
            placeholder = ", ".join(["%s"] * len(item_dict))
            stmt = INSERT_STMT.format(table=table, columns=",".join(item_dict.keys()), values=placeholder)
            cursor.execute(stmt, list(item_dict.values()))
            db.commit()
            id = cursor.lastrowid
            db.close()
            return id
        except Exception as e:
            LOG.error(f"Error inserting into table: {table}, item: {item_dict}. Error: {e}")
        finally:
            db.close()
        return id

    """ --- Specific SQL queries below this section --- """

    def get_weather_codes(self) -> List[tuple]:
        return self.__read__(GET_WEATHER_CODES_QUERY)

    def get_subscription(self, email: str, latitude: float, longitude: float) -> List[tuple]:
        return self.__read__(GET_SUBSCRIPTION_RECORD_QUERY, (email, latitude, longitude))

    def get_subscriptions_by_email(self, email: str) -> List[tuple]:
        return self.__read__(GET_SUBSCRIPTIONS_BY_EMAIL_QUERY, (email,))

    def get_all_subscriptions(self) -> List[tuple]:
        return self.__read__(GET_ALL_SUBSCRIPTIONS_QUERY)

    def update_subscription(self, subscription_id: Optional[int], temp_celsius_above: Optional[float], temp_celsius_below: Optional[float],
                            weather_code: Optional[int], wind_speed_exceeds: Optional[float]) -> None:
        db = self.__connect__()
        cursor = db.cursor()
        cursor.execute(UPDATE_SUBSCRIPTION_QUERY, (temp_celsius_above, temp_celsius_below, weather_code, wind_speed_exceeds, subscription_id))
        db.commit()
        db.close()

    def insert_subscription(self, email: str, latitude: float, longitude: float, location: str) -> int:
        db = self.__connect__()
        cursor = db.cursor()
        cursor.execute(INSERT_SUBSCRIPTION_QUERY, (email, latitude, longitude, location))
        db.commit()
        id = cursor.lastrowid
        db.close()
        return id

    def insert_subscribed_metric(self, subscription_id: Optional[int], temp_celsius_above: Optional[float], temp_celsius_below: Optional[float],
                                 weather_code: Optional[int], wind_speed_exceeds: Optional[float]) -> int:
        db = self.__connect__()
        cursor = db.cursor()
        cursor.execute(INSERT_SUBSCRIPTION_METRIC_QUERY, (subscription_id, temp_celsius_above, temp_celsius_below,
                                                          weather_code, wind_speed_exceeds))
        db.commit()
        id = cursor.lastrowid
        db.close()
        return id

    def delete_subscription(self, subscription_id: int) -> None:
        db = self.__connect__()
        cursor = db.cursor()
        cursor.execute(DELETE_SUBSCRIPTION_QUERY, (subscription_id,))
        db.commit()
        db.close()
