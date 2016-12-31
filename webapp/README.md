# Kortlatalogen - A web app for scanned catalog cards

The application is in the form of a Django project with each individual
card catalog as a Django app within the project.

## Folder structure in kortkatalogen

### kortkatalogen
Django project folder. Project settings are available in the settings.py file.

### shared_templates
Shared template files. Override in <app>/templates if necessary.

### static
Images, CSS-files etc. Does not contain the scanned cards.

### ullas
App for "Ullas tidningskatalog".

