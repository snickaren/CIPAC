# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from cards.models import *
import os
from os import listdir
from os.path import isfile, join
from openpyxl import load_workbook


class Command(BaseCommand):
    help = 'Import card names (from xlsx file). Will overwrite previous card names'
    args = '<xlsx_file_path>'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):

        filepath = args[0]

        #check if path exists
        if not os.path.isfile(filepath):
            raise CommandError("File %s does not exist" % filepath)

        wb = load_workbook(filepath)
        ws = wb.active
        for row in ws.rows:
            filename = row[0].value
            text = row[1].value
            name = row[2].value
            arr = row[3].value
            pseudo = row[4].value
            title = row[5].value
            comment = row[6].value

            if filename is not None:
                try:
                    card = Card.objects.get(filename=filename)
                    card.name = text
                    card.name_tr = name
                    card.arr_tr = arr
                    card.pseudonym_tr = pseudo
                    card.title_tr = title
                    card.comment = comment
                    #card.full_clean()
                    card.save()

                    print "%s\t%s\t%s" % (card.catalog_sequence_number, filename, text)


                except Card.DoesNotExist:
                    print "Not found! Skipped %s" % filename


#                    try:
#                        card = Card.objects.get(box=box, filename=f)
#                    except Card.DoesNotExist:
#                        #make it
#                        card = Card(filename=f,box=box)
#
#                    # parse sequence number in box
#                    sequence_number = int(f.split("_")[-1].replace(".jpg",""))
#                    card.sequence_number=sequence_number
#
#                    # get corresponding ocr file
#                    ocr_filename = f.replace(".jpg","_cleanocr.txt")
#
#                    if os.path.isfile(path + "/" + ocr_filename):
#                        with open(path + "/" + ocr_filename, 'r') as ocrfile:
#                            ocr_text = ocrfile.read()
#
#                        card.ocr_text=ocr_text
#                        card.name=ocr_text.split("\n")[0].strip()
#                    else:
#                        card.name="%s [handskrivet]" % box.label
#
#                    card.save()
