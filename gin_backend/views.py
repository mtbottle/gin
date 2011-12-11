# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers

# import the models
from models import *

# import the controls
import controllers

def index(request):
	return render_to_response("main.html")

def get_all_groups(request):
	''' Return Http request of json with all groups data. '''
	# get all the group data from database and serialize it into json
	groups = controllers.get_all_groups()
	json_data = serializers.serialize("json", groups)

	return HttpResponse(json_data, mimtype="application/son")

def get_all_gips(request):
	''' Return Http request of json with all gip data. '''
	# get all the group data from database and serialize it into json
	gips = controllers.get_all_gips()
	json_data = serializers.serialize("json", gips)

	return HttpResponse(json_data, mimtype="application/son")

def message(request):
	message = Message.objects.all()
	group = Group.objects.all()
	return render_to_response('message.html',{"message":message,"group":group})


def add_message(request):
	r = request.POST
  # For now the message functions also handle the contact medium objects

  # ASSUMPTION! the GIP to associate with the message is that which
  # belongs to the contact medium
	_gip = GIP()
	_contact_medium = ContactMedium.objects.get(description=r['contact_description'])
	if _contact_medium:
		_gip = _contact_medium.gip

  # Furthermore, in the case where the contact medium is not registered,
  # a reference to a GIP will have to be filled too.  For now, expect
  # the view to be passed a GIP_id

  # Whats the best way to create a new entry if one does not
  # exist?
	else:
		_gip = GIP.objects.get(pk=r['GIP_id'])
		_contact_medium = controllers.add_contact_medium(r['contact_type'], r['contact_medium'], _gip, 1)


	controllers.add_message(_gip, _contact_medium, r['routing_origin'], r['message'])

	return render_to_response()

def delete_message(request, message_id):
	controllers.delete_message(Message.objects.get(pk=message_id))

def add_tag(request):
	r = request.POST
	controllers.add_tag(r['tag'], r['description'])

	return render_to_response()

def delete_tag(request, tag_id):
	controllers.delete_tag(Tag.objects.get(pk=tag_id))

	return render_to_response()
