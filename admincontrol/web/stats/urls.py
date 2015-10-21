"""admincontrol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from web.stats.views.authenticate_state import AuthenticateState
from web.stats.views.crawled_stats import CrawlOutputStats
from web.stats.views.document_download_stats import DocumentDownloadedStats
from web.stats.views.extraction_count_stats import ExtractionCountStats
from web.stats.views.extraction_timing_stats import ExtractionStats
from web.stats.views.upload_stats import DocketUploadStats

urlpatterns = [
    url(r'^extraction/timings$', ExtractionStats.as_view(), name='extraction_stats'),
    url(r'^upload/timings$', DocketUploadStats.as_view(), name='upload_stats'),
    url(r'^extraction/count$', ExtractionCountStats.as_view(), name='extraction_count_stats'),
    url(r'^crawl/output$', CrawlOutputStats.as_view(), name='crawl_output_stats'),
    url(r'^downloaded$', DocumentDownloadedStats.as_view(), name='document download stats'),
    url(r'^validate/state', AuthenticateState.as_view(), name='authenticate state'),

]
