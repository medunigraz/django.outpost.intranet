import logging

import requests
from django.apps import apps
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic import View

from . import models
from .conf import settings

logger = logging.getLogger(__name__)


@method_decorator(cache_page(3600), name="dispatch")
class ImageView(View):
    def get(self, request, name, pk):
        try:
            model = apps.get_model("intranet", name)
        except LookupError as e:
            return HttpResponseNotFound(str(e))
        obj = get_object_or_404(model, pk=pk)
        if not hasattr(obj, "get_image"):
            return HttpResponseNotFound(_("Model does not support image publishing."))
        img = obj.get_image()
        if not img:
            return HttpResponseNotFound()
        response = HttpResponse()
        img.save(response, format="webp")
        response["Content-Type"] = "image/webp"
        response["Cache-Control"] = "private,max-age=604800"
        return response
