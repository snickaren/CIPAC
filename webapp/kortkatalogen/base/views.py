# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from base.models import *
from django.db.models import Q

def index(request):

    # TODO: Find all catalogs and list them

    # Read boxes
    return render_to_response('base/index.html', locals())
