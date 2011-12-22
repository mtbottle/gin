# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404

# json parsing
from django.core import serializers
import json

# import the models
from models import *

# import the controls
import controllers

def get_handler_messages(request):
	''' Get all the messages of the groups that belong to the handler '''
	try:
		target_flag = request.REQUEST['target_flag']
		handler_id = int(request.REQUEST['handler_id'])

		groups = controllers.get_groups_of_handler(handler_id)

	except KeyError as e:
		error = {'msg': 'Missing parameters: %s' % e.message}
		return HttpResponse(json.dumps(error), mimetype = 'application/json', status = 400)

	messages = []

	# given the groups, now get all the messages that belong to those groups
	for group in groups:
		msgs = controllers.get_messages_of_group(group.id)
		messages.append(msgs)
		print msgs

	# probably should be render_to_response
	return render_to_response('message.html', {'message': msgs})

def change_priority(request):
	''' What does this function do? '''
	try:
		message_id = int( request.REQUEST['id'] )
		tar_priority=int( request.REQUEST['priority'] )
	except KeyError as e:
		error = {'msg': 'Missing parameters: %s' % e.message}
		return HttpResponse(json.dumps(error), mimetype = 'application/json', status = 400)

	## WHAT DO WE DO WITH THE REQUEST?
	return HttpResponse(content="success")

def change_category(request):
	''' What does this function do? '''
	id_collection = request.REQUEST['id_collection']
	tar = int( request.REQUEST['tar'] )

	if not "," in id_collection:
		m=Message.objects.get(id=int(id_collection))
		m.flag=tar
		m.save()
	else:
		ids=id_collection.split(',')
		for id_ in ids:
			m =Message.objects.get(id=int(id_))
			m.flag=tar
			m.save()
	
	return HttpResponse(content="success")

def get_messages(request):
	''' Given an empty request, return a json of all the messages in '''
	pass

# NO LONGER RENDERING TO HTML...?
#def message(request):
#	''' Is this supposed to get a request? '''
#	Handler_id=1
#	Group_id=1
#	Target_flag=0
#	if request.GET.get('Target_flag'):
#		Target_flag=int(request.GET.get('Target_flag'))
#	if request.GET.get('Handler_id'):
#		Handler_id=int(request.GET.get('Handler_id'))
#	# Handler_id=request.GET.get('Handler_id')
#	group=Group.objects.filter(id__in=(HandlersGroups.objects.filter(handler_ref=Handler_id).values_list('group_ref',flat=True)))

#	if request.GET.get('Group_id'):
#		Group_id=int(request.GET.get('Group_id'))
#	else:
#		Group_id=group.values_list('id',flat=True)[0]

#	message=Message.objects.filter(contact_medium__in=(ContactMedium.objects.filter(gip__in=(GIPGroups.objects.filter(group_ref=Group_id).values_list('gip_ref',flat=True))).values_list('id',flat=True)))
#	return render_to_response('frontend/Gin/message.html',{"message":message,"group":group,"Group_id":Group_id,"Target_flag":Target_flag})


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
	group_id = controllers.create_group(name, location, description)
	response = {'id': group_id}
	return HttpResponse(json.dumps(response), mimetype = 'application/json', status = 200)

def get_all_gips_in_group(request):
	''' Given a post with the group_id structured as : {'group_id': __}
	Return as response of all the gips in the group in json format. '''
	try:
		group_id = int( request.REQUEST['group_id'] )

	# if any of the request items are missing, return HttpResponse of error
	except KeyError as e:
		error = {'msg': 'Missing parameters: %s' % e.message}
		return HttpResponse(json.dumps(error), mimetype = 'application/json', status = 400)

	# get QuerySet of all the database objects
	gips = controllers.get_all_gips_from_group(group_id)
	json_data = serializers.serialize('json', gips)
	return HttpResponse(json_data, mimetype = 'application/json', status = 200)

def get_all_groups(request):
	''' Does not take in a request(?). Return a request with all the groups in json format '''
	# get QuerySet of all groups
	groups = controllers.get_all_groups()
	json_data = serializers.serialize('json', groups)
	return HttpResponse(json_data, mimetype = 'application/json', status = 200)

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


