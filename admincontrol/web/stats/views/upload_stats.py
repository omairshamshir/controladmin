import json
import csv

from django.shortcuts import render
from django.views.generic import View
from dateutil import parser

from web.stats.pymongo_wrapper.extraction_stats import PymongoWrapper


class DocketUploadStats(View):
    template_name = 'upload_stats.html'

    def get(self, request):
        job_delays = []
        upload_times = []
        matcher_times = []
        total_times = []
        state_ids = []

        with open("stats_new.csv") as f:
            rows = csv.DictReader(f)
            for row in rows:
                job_delays.append(abs(float(row["upload_start_delay"])))
                upload_times.append(abs(float(row["time_taken_to_upload"])))
                matcher_times.append(abs(float(row["matcher_time"])))
                total_times.append(abs(float(row["total_time"])))
                state_ids.append(row["state_id"])

        job_start_delay_average = (sum(job_delays) / len(job_delays))
        upload_time_average = (sum(upload_times) / len(upload_times))
        matcher_time_average = (sum(matcher_times) / len(matcher_times))
        total_time_average = (sum(total_times) / len(total_times))

        averages = {
            "jsd": job_start_delay_average,
            "ut": upload_time_average,
            "mt": matcher_time_average,
            "tt": total_time_average

        }

        return render(request, self.template_name, {"total_times": json.dumps(total_times),
                                                    "matcher_times": json.dumps(matcher_times),
                                                    "upload_times": json.dumps(upload_times),
                                                    "job_delays": json.dumps(job_delays),
                                                    "averages": json.dumps(averages),
                                                    "state_ids": json.dumps(state_ids),
                                                    "jsda": job_start_delay_average,
                                                    "uta": upload_time_average,
                                                    "mta": matcher_time_average,
                                                    "tta": total_time_average

                                                    })

    def post(self, request):
        pass
