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

def post_add_new_group(request):
	''' Given a post structured as : {'name':__, 'location': __, 'description': __}
		Create a new group and save it. Return the new group id in response. '''
	try:
		name = request.REQUEST['name']
		location = request.REQUEST['location']
		description = request.REQUEST['description']

	# if any of the request items are missing, return HttpResponse of error
	except KeyError as e:
		error = {'msg': 'Missing parameters: %s' % e.message}
		return HttpResponse(json.dumps(error), mimetype = 'application/json', status = 400)

	# create the database object and return id
	group_id = create_group(name, location, description)
	response = {'id': group_id}
	return HttpResponse(json.dumps(response), mimetype = 'application/json', status = 200)

#def get_all_groups(request):
#	''' Return Http request of json with all groups data. '''
#	# get all the group data from database and serialize it into json
#	groups = controllers.get_all_groups()
#	json_data = serializers.serialize("json", groups)

#	return HttpResponse(json_data, mimtype="application/json")

#def get_all_gips(request):
#	''' Return Http request of json with all gip data. '''
#	# get all the group data from database and serialize it into json
#	gips = controllers.get_all_gips()
#	json_data = serializers.serialize("json", gips)

#	return HttpResponse(json_data, mimtype="application/json")

def message(request):
	message = Message.objects.all()
	group = Group.objects.all()
	return render_to_response('message.html',{"message":message,"group":group})


