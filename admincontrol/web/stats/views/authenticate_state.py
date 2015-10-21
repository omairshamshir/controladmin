import json
import re
import datetime
from datetime import timedelta
from django.shortcuts import render

from django.views.generic import View
from pymongo import MongoClient
from dateutil import parser

from admincontrol.usa import STATES


class AuthenticateState(View):
    template_name = 'authenticate_state.html'
    ip_regex = re.compile("http://(.*)/addversion.json")

    def get(self, request):
        state = request.GET.get("state")
        if not state:
            return render(request, self.template_name, {"data": False, "states": STATES})

        client = MongoClient("mongodb://arbisoft:craw1777@54.225.86.142:27017/puc", 27017)

        db = client["puc"]

        fav_spider_name = "%s_favorites_spider" % state.upper()
        weekly_spider_name = "%s_weekly_spider" % state.upper()

        fav_health, fav_msg = self.is_crawl_healthy(fav_spider_name, db)
        weekly_health, weekly_msg = self.is_crawl_healthy(weekly_spider_name, db)
        is_active, days = self.last_docket(state, db)
        last_counts = self.latest_counts(state, db)

        download_active, date_str, count = self.is_download_active(state, db)

        return render(request, self.template_name, {
            "data": True,
            "states": STATES,
            "fav": fav_health,
            "weak": weekly_health,
            "is_active": is_active,
            "act_days": days,
            "latest_counts": last_counts,
            "dd": download_active,
            "dd_date": date_str,
            "dd_count": count,
            "fav_msg": fav_msg,
            "weekly_msg": weekly_msg,
            "state": state

        })

    def is_download_active(self, state, db):
        data = list(db.document_download_stats.find({"state": state}).sort("_id", -1).limit(7))
        if not data:
            return False, "more than 7 days ago", 0
        for d in data:
            if d["documents_downloaded"] > 0:
                return True, str(d["date"].date()), d["documents_downloaded"]

        return False, "more than 7 days ago", 0

    def latest_counts(self, state, db):
        start_date = datetime.datetime.now() - timedelta(days=4)
        data = list(db.docket_crawl_stats.find({"state": state, "date": {"$gt": start_date}}))
        return data[-1]

    def last_docket(self, state, db):
        docket = list(db.dockets.find({"state": state}).sort('_id', -1).limit(1))

        docket = docket[0]
        crawled_at = parser.parse(docket['crawled_at'])
        crawled_at = crawled_at.replace(tzinfo=None)
        cur_date = datetime.datetime.now()

        days = (cur_date - crawled_at).days

        if days > 1:
            return False, days

        return True, days

    def is_crawl_healthy(self, spider_name, db):

        error_counts = 0
        drop_counts = 0
        item_counts = 0

        datetime_obj = datetime.datetime.now()
        days = 1 if 'fav' in spider_name else 7
        query = db.distributed_weekly_stats.find({"spider_name": spider_name, "start_time": {
            '$gte': (datetime_obj - timedelta(days=days))}}).limit(1).sort('start_time', -1)

        data = list(query)
        if not (data and data[0].get('jobs')):
            return False, "No crawl Found"
        else:
            data = data[0]
            jobs = data.get('jobs', [])
            dur = 0
            for job in jobs:
                error_counts += job['error_count']
                drop_counts += job['drop_count']
                item_counts += job['item_count']
                dur_temp = job.get('duration', 0)
                dur = dur_temp if dur_temp > dur else dur

            if error_counts + drop_counts > 0 or item_counts == 0:
                return False, "Crawler had errors/drops"
            return True, "Crawler ran on time with no errors"
