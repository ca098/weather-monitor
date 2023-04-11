INSERT_STMT = "insert into `{table}` ({columns}) values ({values});"

# =======  Get Queries  ==========
GET_WEATHER_CODES_QUERY = "SELECT id, thunderstorm, drizzle, rain, snow, tornado, clear, clouds FROM weather_monitor.weather_codes LIMIT 1"

GET_LOCATION_BY_NAME_QUERY = (
    "SELECT * FROM weather_monitor.location WHERE location = %s LIMIT 1"
)

GET_SUBSCRIPTION_RECORD_QUERY = "SELECT s.id, s.email, l.latitude, l.longitude, l.location FROM weather_monitor.subscriptions s INNER JOIN weather_monitor.location l ON l.id = s.location_id WHERE s.email = %s AND l.id = %s;"
GET_SUBSCRIPTIONS_BY_EMAIL_QUERY = "SELECT s.id, s.email, l.latitude, l.longitude, l.location, sm.temp_celsius_above, sm.temp_celsius_below, sm.weather_code_equals, sm.wind_speed_exceeds FROM weather_monitor.subscriptions s INNER JOIN weather_monitor.subscribed_metrics sm ON s.id = sm.subscriptions_id INNER JOIN weather_monitor.location l ON s.location_id = l.id WHERE s.email = %s"
GET_ALL_SUBSCRIPTIONS_QUERY = "SELECT s.id, s.email, l.latitude, l.longitude, l.location, sm.temp_celsius_above, sm.temp_celsius_below, sm.weather_code_equals, sm.wind_speed_exceeds FROM weather_monitor.subscriptions s INNER JOIN weather_monitor.subscribed_metrics sm ON s.id = sm.subscriptions_id INNER JOIN weather_monitor.location l ON s.location_id = l.id;"


# =======  Insert Queries  ==========
INSERT_SUBSCRIPTION_METRIC_QUERY = "INSERT INTO weather_monitor.subscribed_metrics (subscriptions_id, temp_celsius_above, temp_celsius_below, weather_code_equals, wind_speed_exceeds) values (%s, %s, %s, %s, %s)"
INSERT_SUBSCRIPTION_QUERY = (
    "INSERT INTO weather_monitor.subscriptions (email, location_id) values (%s, %s)"
)

INSERT_LOCATION_QUERY = "INSERT INTO weather_monitor.location (latitude, longitude, location) values (%s, %s, %s)"

# =======  Delete Queries  ==========
DELETE_SUBSCRIPTION_QUERY = "DELETE FROM weather_monitor.subscriptions WHERE id = %s"
DELETE_SUBSCRIBED_METRIC_QUERY = (
    "DELETE FROM weather_monitor.subscribed_metrics WHERE subscriptions_id = %s"
)

# =======  Update Queries  ==========
UPDATE_SUBSCRIPTION_QUERY = "UPDATE weather_monitor.subscribed_metrics SET temp_celsius_above = %s, temp_celsius_below = %s, weather_code_equals = %s, wind_speed_exceeds = %s WHERE subscriptions_id = %s;"
