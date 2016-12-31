# -*- coding: utf-8 -*-
import datetime
from haystack import indexes
from ullas.models import Card


class CardIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    catalog_sequence_number = indexes.CharField(model_attr='catalog_sequence_number')
    box_label = indexes.CharField(model_attr='box__label')
    updated_at = indexes.DateTimeField(model_attr='updated_at')

    #def prepare_catalogslug(self, obj):
    #    return obj.box.catalog.slug

    def get_model(self):
        return Card

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())
