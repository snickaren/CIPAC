# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from ullas.models import *

class Command(BaseCommand):
    help = 'Generera om sekvensnummer for kort i katalog'
    args = '<catalog_id>'

    def add_arguments(self, parser):
        parser.add_argument('catalog_id')

    def handle(self, *args, **options):

        catalog_id = options['catalog_id']

        # check if catalog exists
        try:
            catalog = Catalog.objects.get(pk = catalog_id)
        except Catalog.DoesNotExist:
            # abort everything
            self.stdout.write("No catalog object found with slug %s. Unable to resequence." % catalog_id)
            raise

        self.stdout.write('Resequencing cards in "%s"' % catalog_id)

        catalog_boxes = catalog.boxes.all().order_by('sequence_number')

        catalog_sequence_number = 1

        for box in catalog_boxes:
            for card in box.cards.all().order_by('sequence_number'):
                card.catalog_sequence_number = catalog_sequence_number
                card.save()
                catalog_sequence_number += 1

        self.stdout.write(self.style.SUCCESS('Done. Last sequence number was %s.' % catalog_sequence_number))
