import os

from appconf import AppConf
from django.conf import settings


class IntranetAppConf(AppConf):
    SHAREPOINT_AUTH = None
    URL = None
    CACHE_IMAGE_TIMEOUT = 300
    BLOG_URL = None
    BLOG_ITEM_URL = None
    BLOG_DESCRIPTION = None
    BLOG_TARGETS = []
    BLOG_COPYRIGHT = None
    BLOG_IMAGE_URL = None
    BLOG_ITEMS = 10
    NEWS_URL = None
    NEWS_ITEM_URL = None
    NEWS_DESCRIPTION = None
    NEWS_TARGETS = []
    NEWS_COPYRIGHT = None
    NEWS_IMAGE_URL = None
    NEWS_ITEMS = 10
    MAILING_URL = None
    MAILING_ITEM_URL = None
    MAILING_DESCRIPTION = None
    MAILING_TARGETS = []
    MAILING_COPYRIGHT = None
    MAILING_ITEMS = 10

    class Meta:
        prefix = "intranet"
