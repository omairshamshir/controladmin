from pymongo import MongoClient

MONGO_IP = "mongodb://arbisoft:craw1777@54.225.86.142:27017/puc"


class PymongoWrapper(object):
    def __init__(self):
        client = MongoClient(MONGO_IP, 27017)
        self.db = client["puc"]

    def get_extraction_stats(self, limit=100):
        extraction_stats = self.db.extraction_stats.find().sort('_id', -1).limit(limit)
        return list(extraction_stats)
