import json

from django.shortcuts import render
from django.views.generic import View
from dateutil import parser

from web.stats.pymongo_wrapper.extraction_stats import PymongoWrapper


class ExtractionStats(View):
    template_name = 'extraction.html'

    def get(self, request):
        pw = PymongoWrapper()
        extraction_stats = pw.get_extraction_stats(50)
        graph_data = []
        blob_names = []
        processing_time_array = []
        processing_delay_array = []

        for e in extraction_stats:
            added_at = parser.parse(e["added_at"])
            processing_time = (e["end_time"] - e["start_time"]).seconds
            processing_delay = (e["start_time"] - added_at).seconds

            # if processing_delay > 21600:
            #     continue

            graph_data.append({
                "blob_name": e["blob_name"],
                "processing_time": processing_time,
                "processing_delay": processing_delay,
            })

            blob_names.append(e["blob_name"])
            processing_time_array.append(processing_time)
            processing_delay_array.append(processing_delay)

        return render(request, self.template_name,
                      {"blob_names": json.dumps(blob_names), "pt_ar": json.dumps(processing_time_array),
                       "pd_ar": json.dumps(processing_delay_array)})

    def post(self, request):
        pass
