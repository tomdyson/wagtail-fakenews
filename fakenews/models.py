from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel


class FakeNewsIndexPage(Page):
    pass


class FakeNewsPage(Page):
    parent_page_types = ["fakenews.FakeNewsIndexPage"]
    year = models.IntegerField("Year")
    author = models.CharField(max_length=250, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL
    )
    introduction = models.TextField(blank=True)
    body = StreamField(
        [
            ("heading", blocks.CharBlock(icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="pilcrow")),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("year"),
        FieldPanel("author"),
        ImageChooserPanel("image"),
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
    ]

    api_fields = [
        APIField("year"),
        APIField("author"),
        APIField("image"),
        APIField(
            "image_thumbnail",
            serializer=ImageRenditionField("width-400", source="image"),
        ),
        APIField("introduction"),
        APIField("body"),
    ]
