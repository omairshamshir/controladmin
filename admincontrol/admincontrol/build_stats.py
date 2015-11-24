import datetime
from datetime import timedelta

from pymongo import MongoClient
import redis

STATES = (
    'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA',
    'MA',
    'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA',
    'RI',
    'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY')

r_server = redis.Redis('54.225.86.142', password='redcraw1777')
client = MongoClient("mongodb://arbisoft:craw1777@54.225.86.142:27017/puc", 27017)
DB = client["puc"]


class BuildStats(object):
    def __init__(self, start_date):
        self.start_date = start_date
        pass

    def data_crawled_stats(self):
        for s in STATES:

            datetime_obj = datetime.datetime.combine(self.start_date, datetime.datetime.min.time())

            if DB.docket_crawl_stats.find_one({"state": s, "date": datetime_obj}):
                continue

            redis_key_base = "%s_%s" % (self.start_date.strftime("%Y%m%d"), s)
            docket_crawled = r_server.lrange("%s_dockets" % redis_key_base, 0, -1)
            filings_crawled = r_server.lrange("%s_filings" % redis_key_base, 0, -1)
            documents_crawled = r_server.lrange("%s_documents" % redis_key_base, 0, -1)

            db_data = {
                "state": s,
                "date": datetime_obj,
                "docket_count": sum([int(d) for d in docket_crawled]),
                "filings_count": sum([int(f) for f in filings_crawled]),
                "documents_count": sum([int(d) for d in documents_crawled]),

            }

            DB.docket_crawl_stats.insert(db_data)

    def document_download_stats(self):
        for s in STATES:

            datetime_obj = datetime.datetime.combine(self.start_date, datetime.datetime.min.time())

            if DB.docket_crawl_stats.find_one({"state": s, "date": datetime_obj}):
                continue

            redis_key = "%s_%s_dd" % (self.start_date.strftime("%Y%m%d"), s)
            docs_downloaded = r_server.lrange(redis_key, 0, -1)

            db_data = {
                "state": s,
                "date": datetime_obj,
                "documents_downloaded": sum([int(d) for d in docs_downloaded]),

            }

            DB.document_download_stats.insert(db_data)


def main():
    days = 30
    for i in xrange(0, days + 1):
        date = datetime.date.today() - timedelta(days=i)
        bs = BuildStats(date)
        print "Current Date: %s" % str(date)
        bs.data_crawled_stats()
        bs.document_download_stats()


if __name__ == '__main__':
    main()
