class Location:
    def __init__(self, db_record):
        self.id = db_record[0]
        self.latitude = db_record[1]
        self.longitude = db_record[2]
        self.location = db_record[3]

    def to_digest_dict(self):
        return {"id": self.id, "lat": self.latitude, "lng": self.longitude}
