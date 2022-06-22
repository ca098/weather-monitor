class Subscription:
    def __init__(self, db_record):
        self.id = db_record[0]
        self.email = db_record[1]
        self.latitude = db_record[2]
        self.longitude = db_record[3]
        self.location = db_record[4]

    def to_digest_dict(self):
        return vars(self)
