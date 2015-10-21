import csv
import urlparse

from pymongo import MongoClient
from datetime import timedelta
from dateutil import parser

import requests

STATES = (
    'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA',
    'MA',
    'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OR', 'PA', 'RI',
    'SC',
    'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY')

client = MongoClient("mongodb://arbisoft:craw1777@54.225.86.142:27017/puc", 27017)
# client = MongoClient("localhost", 27017)
DB = client["puc"]
db = DB["dockets"]

api_auth_key = 'd4dc4045dd431d43b317190a41b982aa'
api_base_url = 'http://pucscrape.appspot.com/'


def get_docket_from_api(state, state_id):
    url = "dockets?api_key=%s&states[]=%s&state_ids[]=%s" % (api_auth_key,
                                                             state, state_id)
    url = urlparse.urljoin(api_base_url, url)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    stats = []
    for s in STATES[:10]:
        print "Working on state", s
        for d in db.find({"state": s}).sort("_id", -1).limit(20):
            if not d.get("end_time") or d.get("end_time") == 'None':
                continue

            if d.get("start_time") == 'None':
                continue

            crawled_at = d['crawled_at']
            upload_start = d['start_time']
            upload_end = d['end_time']

            prod_d = get_docket_from_api(d['state'], d['state_id'])
            on_prod = prod_d['dockets'][0]['updated_at']

            crawled_at_obj_obj = parser.parse(crawled_at).replace(tzinfo=None)
            upload_start_obj = parser.parse(upload_start) - timedelta(seconds=14)
            upload_end_obj = parser.parse(upload_end) - timedelta(seconds=14)
            on_prod_obj = parser.parse(on_prod).replace(tzinfo=None)

            job_d = (upload_start_obj - crawled_at_obj_obj).total_seconds()
            upload_d = (upload_end_obj - upload_start_obj).total_seconds()
            match_d = (on_prod_obj - upload_end_obj).total_seconds()

            total_time = (on_prod_obj - crawled_at_obj_obj).total_seconds()

            out_data = {
                'state': d['state'],
                'state_id': d['state_id'],
                'crawled_at': crawled_at,
                'upload_start': upload_start,
                'upload_complete': upload_end,
                'on_production': on_prod,
                'upload_start_delay': job_d,
                'time_taken_to_upload': upload_d,
                'matcher_time': match_d,
                'filings': prod_d['dockets'][0]['filing_count'],
                'total_time': total_time,
            }
            if total_time < 300:
                stats.append(out_data)
            # if len(stats) > 10:
            #     break

    with open('stats.csv', 'w') as csvfile:
        fieldnames = ["state", "state_id", "crawled_at", "upload_start", "upload_complete", "matcher_time",
                      "on_production", "filings", "total_time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for r in stats:
            writer.writerow(r)


if __name__ == '__main__':
    main()
