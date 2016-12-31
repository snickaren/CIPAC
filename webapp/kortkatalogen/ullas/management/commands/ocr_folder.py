# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from cards.models import *
import os
from os import listdir
from os.path import isfile, join


class Command(BaseCommand):
    help = """Run OCR for a folder of catalog card images. OCR files are saved to
    the same folder as the images and will overwrite previous files. See source
    for tesseract parameters. Requires imagemagick and tesseract."""

    args = '<folder>'

    def add_arguments(self, parser):
        parser.add_argument('folder')

    def handle(self, *args, **options):
        path = args[0]

        self.stdout.write('Running OCR for folder %s.' % path)

        #check if path exists
        if not os.path.isdir(path):
            raise CommandError("Folder %s does not exist. Exiting." % path)

        #

