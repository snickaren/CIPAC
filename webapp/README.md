# Kortlatalogen - A web app for scanned catalog cards

The application a Django project with each individual
card catalog as a Django app within the project.

## Requirements
Python 3.5+, Postgresql.

## Folder structure in kortkatalogen

### kortkatalogen
Django project folder. Project settings are available in the settings.py file.

### shared_templates
Shared template files. Override in app/templates if necessary.

### testscans
Sample Scans and OCR files (based on Ullas catalog) to test import
scripts.

### static
Images, CSS-files etc. Does not contain scanned cards.

### ullas
App for "Ullas tidningskatalog".

### hsnominal
App for "HS nominalkatalog".


## Steps to import card data
After preprocessing and OCR, see the management commands import_nnn.py
in each catalog for information on how to import catalog cards and OCR
files. After importing, run the resequence_nnn.py management command to
generate global card ID:s.


