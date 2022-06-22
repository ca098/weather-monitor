class SubscriptionList:

    def __init__(self, db_record):
        self.subscription_id = db_record[0]
        self.email = db_record[1]
        self.latitude = db_record[2]
        self.longitude = db_record[3]
        self.location = db_record[4]
        self.temp_celsius_above = db_record[5]
        self.temp_celsius_below = db_record[6]
        self.weather_code = db_record[7]
        self.wind_speed_exceeds = db_record[8]

    def to_digest_dict(self):
        return vars(self)
