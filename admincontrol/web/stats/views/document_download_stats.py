import json
import re
import datetime
from datetime import timedelta
from django.shortcuts import render

from django.views.generic import View
from pymongo import MongoClient

from admincontrol.usa import STATES


class DocumentDownloadedStats(View):
    template_name = 'document_downloaded.html'
    ip_regex = re.compile("http://(.*)/addversion.json")

    def get(self, request):
        end_date = datetime.date.today()
        days_list = []
        days = 10

        client = MongoClient("mongodb://arbisoft:craw1777@54.225.86.142:27017/puc", 27017)
        db = client["puc"]
        start_date = datetime.datetime.now() - timedelta(days=days)
        data = list(db.document_download_stats.find({"date": {"$gt": start_date}}))
        ctx_dict = {}
        for d in data:
            date_str = str(d['date'].date())
            if date_str in ctx_dict:
                ctx_dict[date_str][d['state']] = d
            else:
                ctx_dict[date_str] = {d['state']: d}

        for i in xrange(days):
            days_list.append((end_date - timedelta(days=i)).strftime("%Y-%m-%d"))
        days_list = days_list[::-1]

        total_documents_counts = []

        available_days = []

        for d in days_list:
            if not d in ctx_dict:
                continue
            available_days.append(d)

            document_count = 0
            for s in ctx_dict[d].values():
                document_count += s['documents_downloaded']
                s.pop('id', None)
                s.pop('_id', None)
                s.pop('date', None)

            total_documents_counts.append(document_count)

        return render(request, self.template_name, {
            "total_documents": json.dumps(total_documents_counts),
            "date_labels": json.dumps(available_days),
            "states": STATES,
            "complete_ctx": json.dumps(ctx_dict),

        })
