from __future__ import absolute_import, unicode_literals

from django.db import models
from rest_framework import fields as api_fields

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.api import APIField


@register_setting
class CatalogSettings(BaseSetting):
    default_per_page = models.IntegerField(default=50)
    default_product_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE,
        related_name='+', null=True, blank=True
    )
    panels = [
        FieldPanel('default_per_page'),
        ImageChooserPanel('default_product_image'),
    ]


class ServiceIndexPage(Page):
    show_in_menus_default = True

    content_panels = Page.content_panels + [
        InlinePanel('services', label="Servicios"),
    ]

import rest_framework.serializers as api_serializers
class ProductSerializer(api_serializers.Serializer):
    pass

class ProductIndexPage(Page):
    show_in_menus_default = True

    content_panels = Page.content_panels + [
        InlinePanel('products', label="Productos"),
    ]

    # Export fields over the API
    api_fields = [
        APIField('products'),
    ]


class Service(Orderable):
    page = ParentalKey(ServiceIndexPage, related_name='services')

    name = models.CharField(max_length=255, verbose_name='Nombre')
    price = models.FloatField(verbose_name='Precio')
    units = models.CharField(max_length=100, verbose_name='Unidades')


class Product(Orderable):
    page = ParentalKey(ProductIndexPage, related_name='products')

    reference = models.CharField(max_length=255, unique=True, verbose_name="Referencia")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    short_description = RichTextField(null=True, blank=True, verbose_name="Descripción corta")
    long_description = RichTextField(null=True, blank=True, verbose_name="Descripción larga")
    price = models.FloatField(verbose_name="Precio")
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE,
        related_name='+', null=True, blank=True, verbose_name="Imagen del producto"
    )

    # All FieldPanel are defined because ImageChooserPanel is not rendered automatically,
    # so it must be explicitly written, and so all the other fields.
    panels = [
        FieldPanel('reference'),
        FieldPanel('name'),
        FieldPanel('short_description'),
        FieldPanel('long_description'),
        FieldPanel('price'),
        ImageChooserPanel('image'),
    ]

    # Export fields over the API
    api_fields = [
        APIField('reference'),
        APIField('name'),
    ]