import bs4
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from purl import URL

from . import models


class FeedCache:
    lifetime = 1

    def __call__(self, request, *args, **kwargs):
        cache_key = self.get_cache_key(*args, **kwargs)
        response = cache.get(cache_key)

        if response is None:
            response = super().__call__(request, *args, **kwargs)
            cache.set(cache_key, response, self.lifetime)

        return response

    def get_cache_key(self, *args, **kwargs):
        return "%s-%s" % (
            self.__class__.__module__,
            "/".join(["%s,%s" % (key, val) for key, val in kwargs.items()]),
        )


class BlogFeed(FeedCache, Feed):
    title = _("Blog")
    link = settings.INTRANET_BLOG_URL
    description = settings.INTRANET_BLOG_DESCRIPTION
    item_copyright = settings.INTRANET_BLOG_COPYRIGHT
    item_guid_is_permalink = False
    item_enclosure_mime_type = "image/webp"

    def items(self):
        return models.Blog.objects.filter(
            target__contains=settings.INTRANET_BLOG_TARGETS
        ).order_by("-published")[: settings.INTRANET_BLOG_ITEMS]

    def item_title(self, item):
        bs = bs4.BeautifulSoup(item.title, "lxml")
        return bs.text

    def item_description(self, item):
        base_url = URL(settings.INTRANET_URL)
        bs = bs4.BeautifulSoup(item.body, "lxml")
        for e in bs.find_all(True, {"style": True}):
            del e.attrs["style"]
        for e in bs.find_all(True, {"href": True}):
            href = URL(e.attrs.get("href"))
            if not href.scheme():
                url = base_url.path(URL(e.attrs.get("href")).path())
                e.attrs["href"] = url.as_string()
        return "".join([str(x) for x in bs.body.children])

    def item_link(self, item):
        return settings.INTRANET_BLOG_ITEM_URL.format(blog=item)

    def item_guid(self, item):
        return item.pk

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return item.published

    def item_updateddate(self, item):
        return item.modified

    def item_enclosure_url(self, item):
        return item.get_image_url()


class NewsFeed(FeedCache, Feed):
    title = _("News")
    link = settings.INTRANET_NEWS_URL
    description = settings.INTRANET_NEWS_DESCRIPTION
    item_copyright = settings.INTRANET_NEWS_COPYRIGHT
    item_guid_is_permalink = False
    item_enclosure_mime_type = "image/webp"

    def items(self):
        return models.News.objects.filter(
            target__contains=settings.INTRANET_NEWS_TARGETS
        ).order_by("-published")[: settings.INTRANET_NEWS_ITEMS]

    def item_title(self, item):
        bs = bs4.BeautifulSoup(item.title, "lxml")
        return bs.text

    def item_description(self, item):
        base_url = URL(settings.INTRANET_URL)
        bs = bs4.BeautifulSoup(item.body, "lxml")
        for e in bs.find_all(True, {"style": True}):
            del e.attrs["style"]
        for e in bs.find_all(True, {"href": True}):
            href = URL(e.attrs.get("href"))
            if not href.scheme():
                url = base_url.path(URL(e.attrs.get("href")).path())
                e.attrs["href"] = url.as_string()
        return "".join([str(x) for x in bs.body.children])

    def item_link(self, item):
        return settings.INTRANET_NEWS_ITEM_URL.format(news=item)

    def item_guid(self, item):
        return item.pk

    def item_pubdate(self, item):
        return item.published

    def item_updateddate(self, item):
        return item.modified

    def item_enclosure_url(self, item):
        return item.get_image_url()


class MailingFeed(FeedCache, Feed):
    title = _("Mailings")
    link = settings.INTRANET_MAILING_URL
    description = settings.INTRANET_MAILING_DESCRIPTION
    item_copyright = settings.INTRANET_MAILING_COPYRIGHT
    item_guid_is_permalink = False
    item_enclosure_mime_type = "image/webp"

    def items(self):
        return models.Mailing.objects.filter(
            target__contains=settings.INTRANET_MAILING_TARGETS
        ).order_by("-start")[: settings.INTRANET_MAILING_ITEMS]

    def item_title(self, item):
        bs = bs4.BeautifulSoup(item.title, "lxml")
        return bs.text

    def item_description(self, item):
        base_url = URL(settings.INTRANET_URL)
        bs = bs4.BeautifulSoup(item.body, "lxml")
        for e in bs.find_all(True, {"style": True}):
            del e.attrs["style"]
        for e in bs.find_all(True, {"href": True}):
            href = URL(e.attrs.get("href"))
            if not href.scheme():
                url = base_url.path(URL(e.attrs.get("href")).path())
                e.attrs["href"] = url.as_string()
        return "".join([str(x) for x in bs.body.children])

    def item_link(self, item):
        return settings.INTRANET_MAILING_ITEM_URL.format(mailing=item)

    def item_guid(self, item):
        return item.pk

    def item_pubdate(self, item):
        return item.created

    def item_enclosure_url(self, item):
        return item.get_image_url()
