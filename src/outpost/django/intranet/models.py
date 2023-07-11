import logging
from io import BytesIO

import requests
from django.contrib.gis.db import models
from django.contrib.postgres.fields import (
    ArrayField,
    JSONField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from memoize import memoize
from PIL import (
    Image,
    ImageOps,
    UnidentifiedImageError,
)
from purl import URL

from .conf import settings

logger = logging.getLogger(__name__)


class Blog(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    published = models.DateTimeField()
    title = models.TextField()
    body = models.TextField()
    image = models.TextField()
    author = models.TextField()
    target = ArrayField(
        models.TextField(blank=True),
    )

    class Meta:
        managed = False
        db_table = "intranet_blog"
        ordering = ("created",)

    class Refresh:
        interval = 3600

    def __str__(self):
        return self.title

    @memoize(timeout=settings.INTRANET_CACHE_IMAGE_TIMEOUT)
    def get_image(self):
        if self.image:
            url = URL(settings.INTRANET_BLOG_IMAGE_URL).path(self.image)
            try:
                with requests.get(
                    url.as_string(), auth=settings.INTRANET_SHAREPOINT_AUTH
                ) as resp:
                    resp.raise_for_status()
                    return ImageOps.exif_transpose(Image.open(BytesIO(resp.content)))
            except requests.RequestException:
                pass
            except UnidentifiedImageError:
                pass

    def get_image_url(self):
        if self.get_image():
            return reverse(
                "intranet:image",
                kwargs={"name": self.__class__.__name__, "pk": self.pk},
            )


class News(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    published = models.DateTimeField()
    title = models.TextField()
    body = models.TextField()
    image = models.TextField()
    json = JSONField()
    target = ArrayField(
        models.TextField(blank=True),
    )

    class Meta:
        managed = False
        db_table = "intranet_news"
        ordering = ("created",)

    class Refresh:
        interval = 3600

    def __str__(self):
        return self.title

    @memoize(timeout=settings.INTRANET_CACHE_IMAGE_TIMEOUT)
    def get_image(self):
        if self.image:
            url = URL(settings.INTRANET_NEWS_IMAGE_URL).path(self.image)
            try:
                with requests.get(
                    url.as_string(), auth=settings.INTRANET_SHAREPOINT_AUTH
                ) as resp:
                    resp.raise_for_status()
                    return ImageOps.exif_transpose(Image.open(BytesIO(resp.content)))
            except requests.RequestException:
                pass
            except UnidentifiedImageError:
                pass

    def get_image_url(self):
        if self.get_image():
            return reverse(
                "intranet:image",
                kwargs={"name": self.__class__.__name__, "pk": self.pk},
            )


class Mailing(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.TextField()
    short = models.TextField()
    body = models.TextField()
    keywords = ArrayField(
        models.CharField(max_length=128, blank=True),
    )
    members = ArrayField(
        models.CharField(max_length=128, blank=True),
    )
    target = ArrayField(
        models.TextField(blank=True),
    )
    image = models.BinaryField()

    class Meta:
        managed = False
        db_table = "intranet_mailing"
        ordering = ("created",)

    class Refresh:
        interval = 3600

    def __str__(self):
        return self.title

    @memoize(timeout=settings.INTRANET_CACHE_IMAGE_TIMEOUT)
    def get_image(self):
        if self.image:
            try:
                return ImageOps.exif_transpose(Image.open(BytesIO(self.image)))
            except UnidentifiedImageError:
                pass

    def get_image_url(self):
        if self.get_image():
            return reverse(
                "intranet:image",
                kwargs={"name": self.__class__.__name__, "pk": self.pk},
            )
