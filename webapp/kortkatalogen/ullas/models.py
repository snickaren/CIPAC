from django.db import models
from base.models import *
from appconf import AppConf
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

class Box(BaseBox):
    pass


class Card(BaseCard):
    box = models.ForeignKey(Box, related_name="cards", verbose_name="kort")
    search_index = VectorField()
    objects = SearchManager(
        fields = ('name', 'ocr_text', 'ocr_text_back'),
        config = 'pg_catalog.swedish',
        search_field = 'search_index',
        auto_update_search_field = True
    )

    # readonly field to show preview pic in django admin interface
    def image_tag(self):
        return """<img style="width:450px" alt="Kort %s" src="/carddata/%s/%s" />""" % (self.catalog_sequence_number, settings.ULLAS_CARDS_SUBFOLDER, self.box.folder_name + "/" + self.filename)

    def image_tag_back(self):
        if self.filename_back:
            return """<img style="width:450px" alt="Baksida kort %s" src="/carddata/%s/%s" />""" % (self.catalog_sequence_number, settings.ULLAS_CARDS_SUBFOLDER, self.box.folder_name + "/" + self.filename_back)
        else:
            return None

    image_tag.short_description = 'Bild'
    image_tag.allow_tags = True
    image_tag_back.short_description = 'Bild'
    image_tag_back.allow_tags = True




# App specific conf (see http://django-appconf.readthedocs.io/en/latest/)
class UllasConf(AppConf):
    CARDS_SUBFOLDER = "ullas"
