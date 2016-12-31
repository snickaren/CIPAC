# -*- coding: utf-8 -*-
from django.db import models

class BaseCatalog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u"Katalog"
        verbose_name_plural = u"Kataloger"



class BaseBox(models.Model):
    folder_name = models.CharField(max_length=255, unique=True, verbose_name="Katalognamn", help_text="Filkatalog på disk där denna lådas filer ligger")
    sequence_number = models.IntegerField(db_index=True)
    slug = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=255,db_index=True, verbose_name="Etikett")
    catalog = models.ForeignKey(Catalog, related_name="boxes", verbose_name="Tillhör katalog")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.sequence_number, self.label)

    class Meta:
        verbose_name = u"Låda"
        verbose_name_plural = u"Lådor"
        ordering = ['sequence_number']



class BaseCard(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Kortnamn", help_text="Rubriken som visas överst på en kortsida")
    filename = models.CharField(max_length=255, db_index=True, verbose_name="Filnamn", help_text="Filnamnet för bildfilen")
    filename_back = models.CharField(max_length=255, db_index=True, verbose_name="Filnamn baksida", help_text="Filnamnet för bildfilen av baksidan")
    ocr_text = models.TextField(blank=True, help_text="Automatiskt OCR-tolkad text från kortet.")
    ocr_text_back = models.TextField(blank=True, help_text="Automatiskt OCR-tolkad text från kortets baksida.")
    letter = models.CharField(max_length=1, null=True, blank=True, db_index=True, verbose_name="Indexbokstav" , help_text="Anges för första kortet för att dela upp katalogen alfabetiskt.")
    sequence_number = models.IntegerField(db_index=True, verbose_name="Sekvensnummer i låda")
    catalog_sequence_number = models.IntegerField(null=True, blank=True, verbose_name="Kortnummer", help_text="Globalt katalognummer som anger kortets plats i katalogen. Används även som identifierare.")
    box = models.ForeignKey(Box, related_name="cards", verbose_name="Låda")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True, verbose_name="Intern kommentar", help_text="Visas ej för besökare.")


    def __unicode__(self):
        return u'%s %s' % (self.catalog_sequence_number, self.name)

    class Meta:
        verbose_name = u"Kort"
        verbose_name_plural = u"Kort"
        ordering = ['catalog_sequence_number']

