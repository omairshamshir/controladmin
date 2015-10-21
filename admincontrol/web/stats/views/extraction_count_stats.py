import json
import re
import datetime
from datetime import timedelta
from django.shortcuts import render

from django.views.generic import View
import requests


class ExtractionCountStats(View):
    template_name = 'extraction_counts.html'
    ip_regex = re.compile("http://(.*)/addversion.json")

    def get(self, request):
        end_date = datetime.date.today()
        days_list = []
        days = 10
        for i in xrange(days):
            days_list.append((end_date - timedelta(days=i)).strftime("%Y-%m-%d"))
        days_list = days_list[::-1]
        date_labels, count_stats = self.get_extraction_counts(days_list)
        counts = [len(count_stats[d]) for d in date_labels]

        for d in date_labels:
            for s in count_stats[d]:
                s.pop("blob_name")
                s.pop("slug")
                s.pop("document_url")
                s.pop("source_url")

        return render(request, self.template_name,
                      {"count_stats": json.dumps(counts), "date_labels": json.dumps(date_labels),
                       "extraction_stats": json.dumps(count_stats)})

    def get_extraction_counts(self, days_list):
        api_base_url = "http://pucscrape.appspot.com/documents/extracted?api_key=d4dc4045dd431d43b317190a41b982aa&per_page_limit=1000&extracted_after="
        stats_data = {}
        date_labels = []

        for start, end in self.current_next_iterator(days_list):
            date_labels.append(start)
            url = api_base_url + start

            if end:
                url += "&extracted_before=%s" % end

            api_response = requests.get(url)
            stats_data[start] = api_response.json()["documents"]

        return date_labels, stats_data

    def current_next_iterator(self, days_list):
        iterator = iter(days_list)
        item = iterator.next()  # throws StopIteration if empty.
        for next in iterator:
            yield (item, next)
            item = next
        yield (item, None)
