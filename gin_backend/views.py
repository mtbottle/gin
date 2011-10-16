# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404

# import the models
from models import *
from django.db import transaction

def index(request):
  return HttpResponse("Hello World")
