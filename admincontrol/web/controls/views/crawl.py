import subprocess
import time

from django.shortcuts import render, HttpResponse
from django.views.generic import View

from usa import STATES
from admincontrol.script_paths import *


class CrawlView(View):
    template_name = 'crawl.html'

    def get(self, request):
        return render(request, self.template_name, {"states": STATES})

    def post(self, request):
        state = request.POST.get("state")
        crawl_type = request.POST.get("crawl_type")

        log_file_tag = str(int(time.time()))
        log_file_name = "/home/arbisoft/logs/catest%s.txt" % log_file_tag

        if crawl_type.lower() == 'favorites':
            self.run_favorite_crawl(state, log_file_name)

        return HttpResponse("control/log/%s" % log_file_tag)

    def run_favorite_crawl(self, state, log_file_name):
        args = "python %s -s %s &> %s" % (FAVORITE_CRAWL_PATH, state, log_file_name)

        # subprocess.Popen(args, shell=True, env={"PYTHONPATH": "/Users/omairshamshir/Documents/github/puctools/lib",
        #                                         "HOME": "/Users/omairshamshir"}, )

        subprocess.Popen(args, shell=True)

        time.sleep(5)

    def run_weekly_crawl(self, state, log_file_name):
        pass
