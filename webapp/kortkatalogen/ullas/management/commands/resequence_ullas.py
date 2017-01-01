# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from ullas.models import *

class Command(BaseCommand):
    help = 'Regenerate global sequence numbers for cards'

    def handle(self, *args, **options):

        self.stdout.write('Resequencing cards')

        catalog_boxes = Box.objects.all().order_by('sequence_number')

        catalog_sequence_number = 1

        for box in catalog_boxes:
            for card in box.cards.all().order_by('sequence_number'):
                card.catalog_sequence_number = catalog_sequence_number
                card.save()
                catalog_sequence_number += 1

        self.stdout.write(self.style.SUCCESS('Done. Last sequence number was %s.' % catalog_sequence_number))
