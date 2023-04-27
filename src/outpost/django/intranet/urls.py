from django.urls import (
    path,
    re_path,
)

from . import (
    feeds,
    views,
)

app_name = "intranet"

urlpatterns = [
    path("blog/feed.atom", feeds.BlogFeed()),
    path("news/feed.atom", feeds.NewsFeed()),
    path("mailing/feed.atom", feeds.MailingFeed()),
    path(
        "image/<str:name>/<int:pk>",
        views.ImageView.as_view(),
        name="image",
    ),
]
