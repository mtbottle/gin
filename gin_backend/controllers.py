# import the models
from models import *
from django.db import transaction

# import a way to extend lists/queryset into lists
from itertools import chain

# HANDLER functions
def get_handler(handler_id):
	''' Given:  handler_id -      int
			Return handler django object '''
	return Handler.objects.get(id = handler_id)

def delete_gip(gip_id): 
	''' Given:  gip_id -          int
			Return nothing. Removes the GIP django object at gip_id from database '''
	gip = GIP.objects.get(id=gip_id)
	gip.delete()  

def edit_gip(gip_id, new_data):
	''' Do we really need this? GIP only stores registration info right now... I guess this might be useful when we add more stuff to GIP

			Given:  gip_id -          int
							new_data -        dictionary of new values
			Return nothing. Edits the GIP django object at gip_id with new_data '''
	gip = GIP.objects.get(gipID=gip_id)
	# Maybe iterate through request hash and update the fields which are passed?
	# This would place more burden on views.py but make the code easier to
	# maintain
	for u in new_data: # rename this
		gip.__dict__[u] = new_data[u]
	gip.save()

	# OR return the GIP object to be handled by view.py (not intuitive to me)
	#  return _gip
	
def change_password(handler_id, new_password):
	''' Given: handler_id -     int
						 new_password -   string
			Return the handler object with the password changed '''
	handler = Handler.objects.get(id = handler_id)
	handler.password = encode_password(new_password)
	handler.save()
	return handler
	
def change_location(handler_id, new_location):
	''' Given:  handler_id -    int
							new_location -  string
			Return handler with the location updated. '''
	handler = Handler.objects.get(id = handler_id)
	handler.location = new_location
	handler.save()
	return handler
	

def add_new_GIP():
	''' Return a new GIP django object '''
	gip = GIP(self_register=0)
	gip.save()
	return gip
	

def get_groups_of_handler(handler_id):
	''' Given a handler_id, return a list of group ids of which the handler belongs to '''
	# extract all the Handler/Group references
	handler = Handler.objects.get(id = handler_id)
	refs = HandlersGroups.objects.filter(handler_ref = handler)

	ref_ids = map( lambda x: x.id, refs )

	handler_groups = []

	# extract the groups that have group_ref in refs
	for ref_id in ref_ids:
		handler_group = Group.objects.get(id = ref_id)
		handler_groups.append(handler_group)

	return handler_groups
	
#####

# HEAD OFFICE functions
def create_admin(handler_id):
	''' Given:  handler_id (int)
		Return a new system admin object that references object at handler_id '''
	handler = Handler.objects.get(id = handler_id)

	try:
		sys_admin = SystemAdmin(handler_ref = handler)
	# if the handler is already a system admin, just return the system admin object
	except:
		sys_admin = SystemAdmin.objects.get(handler_ref = handler)
	return sys_admin

def add_new_handler(n, loc):
	''' Given:  n  (string), loc (string)
		Return a new handler django object with name n and location loc'''
	try:
		handler = Handler(name=n, location=loc)
		handler.save()
	except:
		handler = Handler.objects.get(name=n, location=loc)

	return handler
	
def delete_handler(handler_id):
	''' Given:  handler_id -        int
			Return nothing. Removes the handler django object at handler_id from database. '''
	try:
		handler = Handler.objects.get(id = handler_id)
		handler.delete()
	except:
		print "%d does not exist" % handler_id
	
# Not sure how to implement groups
def move_handler_to_group(handler_id, group_id):
	''' Given:  handler_id -        int
							group_id -          int
			Return nothing. Add a relation between handler at handler_id and group at group_id (add handler to group) '''
	handler = Handler.objects.get(id = handler_id)
	group = Group.objects.get(id = group_id)

	# try to get the reference from database, but create it otherwise
	try:
		HandlersGroups.objects.get(group_ref = group, handler_ref = handler)
	except:
		# don't really need the group/handler ids?
		relation = HandlersGroups()
		relation.group_ref = group
		relation.handler_ref = handler
	
def message_group_handlers(request):
	''' TODO:  I don't think this needs to be a backend/database thing? Perhaps send out message given a message... sendmail?'''
	pass

	
#####

# SYSTEM ADMIN functions
def create_group(n, loc, d):
	''' Given a name, n, and location, loc, create a group with those attributes and save it in the database. Return the django group object '''
	g = Group(name=n, location=loc, description=d)
	g.save()
	return g.id
	
def delete_group(group_id):
	''' Perhaps we should be matching with name/location instead? 
	Given a group id, remove it from the database '''
	Group.objects.get(id = group_id).delete()
	
def edit_group(group_id, edit_params):
	''' Given a group id and a dictionary of parameters to edit as edit_param,
			iterate through all the parameters of the dictionary and modified the value
			of that database entry in database. Return nothing.'''  
	group = Group.object.get(id = group_id)
	for param, value in edit_params:
		group.param = value

	group.save()
	
def get_group(group_id):
	''' Given:  group_id -            int
			Return group django object associated with group_id'''
	group = Group.objects.get(id = group_id)
	return group
	
def get_all_groups():
	''' Return all the group django objects from database. This is a django queryset object.'''
	return Group.objects.all()
	
def get_all_gips():
	''' Return all the GIP django objects from database. This is a django queryset object. '''
	return GIP.objects.all()
		
	
def get_all_handlers():
	''' Return all the handler django objects from database. This is a django queryset object. '''
	return Handler.objects.all()  

#####

# GROUP functions

def add_gip_to_group(gip_id, group_id):
	''' Given:  gip_id -              int
							group_id -            int
			Return nothing. Create a relation between GIP and group (add gip to group) '''
	gip = GIP.objects.get(id = gip_id)
	group = Group.objects.get(id = group_id)

	try:
		GIPGroups.objects.get(gip_ref = gip, group_ref = group)
	except:
		relation = GIPGroups()
		relation.gip_ref = gip
		relation.group_ref = group
		relation.save()
	 
def delete_gip_from_group(gip_id, group_id):
	''' Given:  gip_id -              int
							group_id -            int
			Return nothing. Removes the relation between GIP and group at the given ids '''
	GIPGroups.objects.get(gip_ref__id = gip_id, group_ref__id = group_id).delete()

def edit_location(group_id, loc):
	''' Given location information, and a group id, update the location for 
			the group object with group id '''
	group = Group.objects.get(id = group_id)
	group.location = loc
	group.save()

def edit_group_description(group_id, n):
	''' Given a description (name), update the description of the group object with
			the given group id '''
	group = Group.objects.get(id = group_id)
	group.name = n
	group.save()

def add_handler_to_group(handler_id, group_id):
	''' Given a handler and group object, create a relation between handler and group '''
	handler = Handler.objects.get(id = handler_id)
	group = Group.objects.get(id = group_id)

	try:
		HandlersGroups.objects.get(hander_ref = handler, group_ref = group)
	except:
		hgr = HandlersGroups()
		hgr.handler_ref = handler
		hgr.group_ref = group
		hgr.save()

def delete_handler_from_group(handler, group):
	''' Given a handler id and group id, remove the relation that says that the 
			handler belongs to the group. '''
	HandlerGroup.objects.get(handler_ref = handler, group_ref = group).delete()

def get_all_gips_from_group(group_id):
	''' Given a group id, return all the GIPS who are associated with the handlers as a QuerySet'''
	# extract all the gips from group
	gips_ref = GIPGroups.objects.filter(group_ref = group_id)

	return gips_ref

def get_all_handlers_from_group(group_id):
	''' Given a group id, return all the handlers who are in the group with group_id as a list'''
	# extract all the handlers in a particular group  
	handlers_ref = HandlersGroups.objects.filter(group_ref = group_id)

	return handlers_ref


#####

def flag_message(handler_id, message_id):
	''' Given a handler_id and message_id, create a relation between the two objects. '''
	# extract all the objects
	message = Message.objects.get(id = message_id)
	handler = Handler.objects.get(id = handler_id)

	try:
		HandlerFlagMessage.objects.get(message_ref = message, handler_ref = handler)
	except:
		flg = HandlerFlagMessage()
		flg.handler_ref = handler
		flg.message_ref = message
		flg.save()

def return_handler_flagged_message(handler_id):
	''' Given a handler_id, return all message objects that has been flagged by handler as django's queryset object. '''
	handler = Handler.objects.get(id = handler_id)
	messages = HandlerFlagMessage.objects.filter(handler_ref = Handler)
	return messages

# Message and tag related functions

def get_all_messages():
	''' Return all the messages in database as a QuerySet object '''
	return Message.objects.all()

def edit_entry(entry, new_data):
	''' Edit general object details. Elements of the object to be updated are passed as a hash keyed by element name. '''
	for update in new_data:
		entry.__dict__[update] = new_data[update]
	entry.save()

def add_message(gip_id, contact_medium_id, routing_origin, message):
	''' Create a message entry associated with a given GIP and contact medium '''
	_gip = GIP.objects.get(id = gip_id)
	_contact_medium = ContactMedium.objects.get(id = contact_medium_id)
	m = Message(gip=_gip, message=message, datetime_sent=datetime.datetime.now(), contact_medium=_contact_medium, flag=0, routing_origin=routing_origin)
	m.save()


def delete_message(message_id):
	''' Delete a message given a reference to the messase object '''
	Message.objects.get(id = message_id).delete()


def add_tag(_tag, _description):
	''' Add a tag with description '''
	t = Tag(tag=_tag, description=_description)
	t.save()


def delete_tag(tag_id):
	''' Delete tag given reference to the object '''
	Tag.objects.get(id = tag_id).delete()

def add_contact_medium(contact_type, description, gip_id, preferred_contact):
	''' Add a contact medium, associated with a given gip '''
	_gip = GIP.objects.get(id = gip_id)
	c = ContactMedium(contact_type, description, _gip, preferred_contact)
	c.save()


def change_gip_for_contact_medium(contact_medium_id, gip_id):
	''' Change the GIP associated with a contact_medium '''
	gip = GIP.objects.get(id = gip_id)
	contact_medium = ContactMedium.objects.get(id = contact_medium_id)
	contact_medium.gip_ref = gip
	contact_medium.save()

def delete_contact_medium(contact_medium_id):
	''' Delete contact medium entry '''
	ContactMedium.objects.get(id = contact_medium_id).delete()


def add_message_tag(message_id, tag_id):
	''' Add a reference to a tag for a message '''
	message = Message.objects.get(id = message_id)
	tag = Tag.objects.get(id = tag_id)
	r = MessageTag(message, tag)
	r.save()
	return r

def delete_message_tag(message_id, tag_id):
	''' Delete a reference to a tag for a message '''
	message = Message.objects.get(id = message_id)
	tag = Tag.objects.get(id = tag_id)

	MessageTag.objects.get(message_ref=Message, tag_ref=tag).delete()

def get_all_messages_for_tag(tag):
	''' Return a list of message objects for a given tag '''
	messageTags = MessageTag.objects.filter(tag_ref=tag)
	messages = []
	for ref in messageTags:
		messages.append(ref.message_ref)

	return messages

def get_tags_for_message(message_id):
	''' Return a list of tags for a given message '''
	message = Message.objects.get(id = message_id)

	messageTags = MessageTag.objects.filter(message_ref=message)
	tags = []
	for ref in messageTags:
		tags.append(ref.tag_ref)
  
	return tags

def get_messages_of_gip(gip_id):
	''' Given a gip_id, get all the messages that the gip wrote through all his contact mediums. Return a list of messages '''
	gip = GIP.objects.get(id = gip_id)
	
	# get all the contact mediums that belongs to the gip
	cms = ContactMedium.objects.filter(gip = gip)
	
	messages = []
	# iterate through all contact mediums and extract all the messages
	for cm in cms:
		msgs = Message.objects.filter(contact_medium = cm)
		# convert the list of messages into a proper queryset_object
		messages = list(chain(messages, msgs))

	return messages


def get_messages_of_group(group_id):
	''' Given a group_id, get the messages that belong to the group by going through all the gips and extracting the messages that belongs to the gips '''
	group = Group.objects.get(id = group_id)
	print group

	# get all the gips that belongs to that group
	gip_relations = GIPGroups.objects.filter(group_ref = group)
	print GIPGroups.objects.all()
	gips = map( lambda x: GIP.objects.get(id = x.gip_ref_id), gip_relations)

	print gip_relations

	messages = []
	# now get all the messages of each gip and get their messages
	for gip in gips:
		msgs = get_messages_of_gip(gip.id)
		messages = list(chain(messages, msgs))

	return messages


