from django.db import models
from wagtail.core.models import Page

from wagtail.core.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel#, PageChooserPanel
from wagtail.core.fields import StreamField



class HomePage(Page):
   
    subtitle = models.CharField(max_length=100, blank=False, null=True)
    content = StreamField(
        [
            ('paragraph', RichTextBlock()),
            ('image', ImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )

    max_count = 1    

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = 'Домашняя страница'
