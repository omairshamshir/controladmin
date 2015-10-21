import csv
from pymongo import MongoClient
from dateutil import parser

import datetime
from datetime import timedelta

 # client = MongoClient("localhost", 27017)
DB = client["puc"]
db = DB["extraction_stats"]

times = []
stats = []

for r in db.find():
    added_at = parser.parse(r['added_at'])
    if added_at > (datetime.datetime.now() - timedelta(days=1)):
        extraction_started = r['start_time']
        total_time = (extraction_started - added_at).total_seconds()
        times.append(total_time)
        print r['blob_name']
        print total_time

        stats.append({
            "blob_name": r['blob_name'],
            "added_at": r['added_at'],
            "extraction_starts": r["start_time"],
            "extraction_ends": r["end_time"],
            "time_to_extract": (r["end_time"] - r["start_time"]).total_seconds(),
            "total_time_seconds": total_time,
            "total_time": total_time / (3600),
        })

print min(times)
print max(times)
print sum(times) / len(times)

with open('extraction_stats.csv', 'w') as csvfile:
    fieldnames = ["blob_name", "added_at", "extraction_starts", "extraction_ends", "time_to_extract",
                  "total_time_seconds", "total_time"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in stats:
        writer.writerow(r)
