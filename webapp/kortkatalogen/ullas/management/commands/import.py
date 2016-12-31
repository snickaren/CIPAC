# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from ullas.models import *
import os
from os import listdir
from os.path import isfile, join
import glob

class Command(BaseCommand):
    help = 'Import folders of catalog cards.'
    args = '<path> <catalog_id>'

    def add_arguments(self, parser):
        parser.add_argument('path')
        parser.add_argument('catalog_id', type=int)

    def handle(self, *args, **options):

        path = options['path']
        catalog_id = options['catalog_id']

        self.stdout.write("Importing %s to catalog %s" % (path, catalog_id))

        #check if path exists
        if not os.path.isdir(path):
            raise CommandError("Path %s does not exist" % path)

        # check if catalog exists
        try:
            catalog = Catalog.objects.get(pk = catalog_id)
        except Catalog.DoesNotExist:
            # abort everything
            self.stdout.write("No catalog object found with id %s. Unable to import data." % catalog_id)
            raise

        # list box folders in path
        box_folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

        for folder in box_folders:

            self.stdout.write("Importing %s" % folder)

            #check if folder name exists
            try:
                box = Box.objects.get(folder_name=folder, catalog=catalog)
                self.stdout.write("Loaded existing box %s" % box.id)

            except Box.DoesNotExist:

                # make it - assumes folder name
                # <sequence number>_<label>
                # e.g. 01_K-So

                self.stdout.write(folder)
                sequence_number = int(folder.split("_")[0])
                label = folder.split("_")[1]

                box = Box(folder_name=folder,
                        sequence_number=sequence_number,
                        label=label,
                        slug=label,
                        catalog=catalog)
                box.save()

                self.stdout.write(self.style.SUCCESS("Created box %s" % box.id))


            #import folder content and create cards
            scanfiles = [f for f in sorted(glob.glob(os.path.join(path, folder, "*.jpg"))) if not f.endswith(".clean.jpg")]

            # iterate over file pairs
            for i in range(0, len(scanfiles), 2):
                front = scanfiles[i]
                back = scanfiles[i+1]
                f = os.path.split(front)[1]

                try:
                    card = Card.objects.get(box=box, filename=f)
                except Card.DoesNotExist:
                    card = Card(filename=f,box=box)

                # parse card sequence number in box
                sequence_number = int(f.split("_")[-1].replace(".jpg",""))
                card.sequence_number=sequence_number

                # get corresponding ocr file
                ocr_filename = f.replace(".jpg",".jpg.clean.jpg.txt")

                if os.path.isfile(os.path.join(path, folder, ocr_filename)):
                    with open(os.path.join(path, folder, ocr_filename), 'r') as ocrfile:
                        ocr_text = ocrfile.read()

                    card.ocr_text=ocr_text
                    card.name=sequence_number

                # backside
                card.filename_back = os.path.split(back)[1]
                ocr_filename_back = card.filename_back.replace(".jpg",".jpg.clean.jpg.txt")

                if os.path.isfile(os.path.join(path, folder, ocr_filename_back)):
                    with open(os.path.join(path, folder, ocr_filename_back), 'r') as ocrfile:
                        ocr_text = ocrfile.read()

                    card.ocr_text_back=ocr_text

                card.save()
