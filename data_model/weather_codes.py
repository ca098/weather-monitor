class WeatherCodes:
    def __init__(self, db_record):
        self.weather_code_id = db_record[0]
        self.thunderstorm = db_record[1]
        self.drizzle = db_record[2]
        self.rain = db_record[3]
        self.snow = db_record[4]
        self.tornado = db_record[5]
        self.clear = db_record[6]
        self.clouds = db_record[7]

    def to_digest_dict(self):
        return {
            "thunderstorm": self.thunderstorm,
            "drizzle": self.drizzle,
            "rain": self.rain,
            "snow": self.snow,
            "tornado": self.tornado,
            "clear": self.clear,
            "clouds": self.clouds,
        }
