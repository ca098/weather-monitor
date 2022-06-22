

INSERT_STMT = 'insert into `{table}` ({columns}) values ({values});'

# =======  Get Queries  ==========

GET_WEATHER_CODES_QUERY = 'SELECT id, thunderstorm, drizzle, rain, snow, tornado, clear, clouds FROM tmonitor.weather_codes LIMIT 1'
GET_SUBSCRIPTION_RECORD_QUERY = 'SELECT id, email, latitude, longitude, location FROM tmonitor.subscriptions WHERE email = %s AND latitude = %s AND longitude = %s;'
GET_SUBSCRIPTIONS_BY_EMAIL_QUERY = 'SELECT s.id, s.email, s.latitude, s.longitude, s.location, sm.temp_celsius_above, sm.temp_celsius_below, sm.weather_code_equals, sm.wind_speed_exceeds FROM tmonitor.subscriptions s INNER JOIN tmonitor.subscribed_metrics sm ON s.id = sm.subscriptions_id WHERE s.email = %s'
GET_ALL_SUBSCRIPTIONS_QUERY = 'SELECT s.id, s.email, s.latitude, s.longitude, s.location, sm.temp_celsius_above, sm.temp_celsius_below, sm.weather_code_equals, sm.wind_speed_exceeds FROM tmonitor.subscriptions s INNER JOIN tmonitor.subscribed_metrics sm ON s.id = sm.subscriptions_id;'


# =======  Insert Queries  ==========
INSERT_SUBSCRIPTION_QUERY = 'INSERT INTO tmonitor.subscriptions (email, latitude, longitude, location) values (%s, %s, %s, %s)'
INSERT_SUBSCRIPTION_METRIC_QUERY = 'INSERT INTO tmonitor.subscribed_metrics (subscriptions_id, temp_celsius_above, temp_celsius_below, weather_code_equals, wind_speed_exceeds) values (%s, %s, %s, %s, %s)'

# =======  Delete Queries  ==========
DELETE_SUBSCRIPTION_QUERY = 'DELETE FROM tmonitor.subscriptions WHERE id = %s'
DELETE_SUBSCRIBED_METRIC_QUERY = 'DELETE FROM tmonitor.subscribed_metrics WHERE subscriptions_id = %s'

# =======  Update Queries  ==========
UPDATE_SUBSCRIPTION_QUERY = 'UPDATE tmonitor.subscribed_metrics SET temp_celsius_above = %s, temp_celsius_below = %s, weather_code_equals = %s, wind_speed_exceeds = %s WHERE subscriptions_id = %s;'
