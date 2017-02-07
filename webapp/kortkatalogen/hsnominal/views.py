# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from hsnominal.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def about(request):
    # Read boxes
    return render_to_response('hsnominal/about.html', locals())


def index(request):

    # Read alphabet index cards
    index_cards = Card.objects.filter(letter__isnull=False).exclude(letter='').order_by("letter")

    # Read boxes
    return render_to_response('hsnominal/index.html', locals())


def search(request):
    if request.GET.get("q"):
        query = request.GET.get("q", None)
        result = Card.objects.search(query)[:100]
        paginator = Paginator(result, 20)

        pageno = request.GET.get('page')

        try:
            page = paginator.page(pageno)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page = paginator.page(paginator.num_pages)

    return render_to_response('hsnominal/search.html', locals())


def browse(request, card_catalog_sequence_number):
    card = Card.objects.get(catalog_sequence_number=card_catalog_sequence_number)
    box = card.box
    box_cards = box.cards.all().only("catalog_sequence_number", "name") #for right column list display
    image_url = box.folder_name + "/" + card.filename
    fullres_image_url = box.folder_name + "/" + card.filename
    image_back_url = box.folder_name + "/" + card.filename_back
    fullres_image_back_url = box.folder_name + "/" + card.filename_back

    # find next and previous card
    try:
        previous_card = Card.objects.get(catalog_sequence_number=card.catalog_sequence_number - 1)
    except Card.DoesNotExist:
        previous_card = None

    try:
        next_card = Card.objects.get(catalog_sequence_number=card.catalog_sequence_number + 1)
    except Card.DoesNotExist:
        next_card = None

    # find +10 and -10 cards
    try:
        previous10_card = Card.objects.get(catalog_sequence_number=card.catalog_sequence_number - 10)
    except Card.DoesNotExist:
        previous10_card = None

    try:
        next10_card = Card.objects.get(catalog_sequence_number=card.catalog_sequence_number + 10)
    except Card.DoesNotExist:
        next10_card = None


    # next and previous box
    try:
        previous_box_card = Card.objects.filter(box__sequence_number = box.sequence_number - 1)[0]
    except:
        previous_box_card = None

    try:
        next_box_card = Card.objects.filter(box__sequence_number = box.sequence_number + 1)[0]
    except:
        next_box_card = None

    return render_to_response('hsnominal/browse.html', locals())



