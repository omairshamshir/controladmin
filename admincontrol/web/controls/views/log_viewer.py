import re
from django.shortcuts import render

from django.views.generic import View


class LogView(View):
    template_name = 'logs.html'
    ip_regex = re.compile("http://(.*)/addversion.json")

    def get(self, request, name):

        with open("static/logs/%s.txt" % name) as f:
            log_text = f.read()

        scrapyd_inst_ips = self.ip_regex.findall(log_text)
        inst_details = []

        instance_count = 1

        for ip in scrapyd_inst_ips:
            inst_details.append({
                "name": "Instance %d" % instance_count,
                "url": "http://%s/jobs" % ip

            })
            instance_count += 1

        return render(request, self.template_name, {"lines": log_text.split("\n"), "instances": inst_details})
