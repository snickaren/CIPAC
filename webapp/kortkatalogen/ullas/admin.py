# -*- coding: utf-8 -*-
from django.contrib import admin
from ullas.models import *
from django.forms import Textarea


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'box_name', 'order', 'catalog_sequence_number', 'filename', 'ocr_text', 'letter', 'updated_at')
    search_fields = ['catalog_sequence_number', 'filename', 'name', 'ocr_text']
    readonly_fields = ('image_tag', 'image_tag_back')
    fieldsets = (
        (None, {
            'fields': ['name', 'catalog_sequence_number', 'filename', 'filename_back', 'letter', 'sequence_number']
        }),
        ('OCR', {
            'classes': ('ocr_fields',),
            'fields': [('ocr_text', 'image_tag'), ('ocr_text_back', 'image_tag_back')],
        }),
        (None, {
            'fields': ['comment',]
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                           attrs={'rows': 16,
                                  'cols': 35,
                                  'style': 'width: 90%'})},
    }

    def order(self, instance):
        return str(instance.box.folder_name) + "-" + str(instance.sequence_number)

    def box_name(self, instance):
        return instance.box.folder_name


class BoxAdmin(admin.ModelAdmin):
    list_display = ('folder_name', 'catalog_name', 'sequence_number', 'label', 'updated_at')

    def catalog_name(self, instance):
        return instance.catalog.name


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Card, CardAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Catalog, CatalogAdmin)
