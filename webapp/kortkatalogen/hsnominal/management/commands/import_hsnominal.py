# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from hsnominal.models import *
import os
from os import listdir
from os.path import isfile, join
import glob



class Command(BaseCommand):
    help = 'Import folders of catalog cards.'
    args = '<path>'

    def add_arguments(self, parser):
        parser.add_argument('path')


    def handle(self, *args, **options):
        path = options['path']

        self.stdout.write("Importing %s to catalog" % path)

        #check if path exists
        if not os.path.isdir(path):
            raise CommandError("Path %s does not exist" % path)

        # list box folders in path
        box_folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

        for folder in box_folders:

            self.stdout.write("Importing %s" % folder)

            #check if folder name exists
            try:
                box = Box.objects.get(folder_name=folder)
                self.stdout.write("Loaded existing box %s" % box.id)

            except Box.DoesNotExist:

                # make it - assumes folder name
                # <sequence number>_<label>
                # e.g. 01_K-So

                self.stdout.write("Creating %s " % folder)
                sequence_number = int(folder.split("_")[0])
                label = folder.split("_")[1]

                box = Box(folder_name=folder,
                        sequence_number=sequence_number,
                        label=label,)
                box.save()

                self.stdout.write(self.style.SUCCESS("Created box %s" % box.id))


            #import folder content and create cards
            scanfiles = [f for f in sorted(glob.glob(os.path.join(path, folder, "*.jpg"))) if not "clean" in f]
            self.stdout.write(self.style.SUCCESS("Found %s files" % len(scanfiles)))

            # iterate over files
            for imagepath in scanfiles:
                f = os.path.split(imagepath)[1]

                try:
                    card = Card.objects.get(box=box, filename=f)
                except Card.DoesNotExist:
                    card = Card(filename=f,box=box)

                # parse card sequence number in box from filename
                sequence_number = int(f.split("_")[-1].replace(".jpg",""))
                card.sequence_number=sequence_number

                # get corresponding ocr file
                ocr_filename = f.replace(".jpg",".jpg.txt.clean.txt")

                if os.path.isfile(os.path.join(path, folder, ocr_filename)):
                    with open(os.path.join(path, folder, ocr_filename), 'r') as ocrfile:
                        ocr_text = ocrfile.read()

                    card.ocr_text=ocr_text
                    #card.name=sequence_number

                card.save()
                self.stdout.write(self.style.SUCCESS("Created card %s" % card.id))
