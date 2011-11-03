# import the models
from models import *
from django.db import transaction


# HANDLER functions
def get_handler(handler_id):
  ''' Given a handler id, get that handler object from handler table '''
  return Handler.objects.get(id=handler_id)

def delete_GIP(gip_id): 
  ''' Given a gip id, get that gip object from the gip table '''
  GIP.objects.get(gipID=gip_id).delete()
  
def edit_GIP(gip_id, new_data):
  gip = GIP.objects.get(gipID=gip_id)
  # Maybe iterate through request hash and update the fields which are passed?
  # This would place more burden on views.py but make the code easier to
  # maintain
  for u in new_data: # rename this
    gip.__dict__[u] = new_data[u]
  gip.save()

  # OR return the GIP object to be handled by view.py (not intuitive to me)
  #  return _gip

def get_name(gip_id):
  gip = GIP.objects.get(gipID=gip_id)
  return gip.name
  
def change_password(n, new_password):
  ''' Given the name, n, and a new password, save the password for user with name, n. '''
  handler = Handler.objects.get(name=n)
  handler.password = new_password
  handler.save()
  return handler
  
def change_location(n, new_location):
  handler = Handler.objects.get(name=n)
  handler.location = new_location
  handler.save()
  return handler
  

def add_new_GIP(gip_id):
  ''' Create a new gip and add it to the database '''
  gip = GIP(gipID=gip_id, self_register=0)
  gip.save()
  return gip
  
#####

# HEAD OFFICE functions
def add_new_handler(n, loc):
  handler = Handler(name=n, location=loc)
  handler.save()
  return handler
  
def delete_handler(n):
  handler = Handler.objects.get(name=n)
  handler.delete()
  return handler
  
# Not sure how to implement groups
def move_handler_to_group(handler_id, group_id):
  handler = Handler.objects.get(id = handler_id)
  group = Group.objects.get(id = group_id)
  # don't really need the group/handler ids?
  relation = GroupHandler()
  relation.group_ref = group
  relation.handler_ref = handler
  
def message_group_handlers(request):
  ''' ? I don't think this needs to be a backend/database thing? Perhaps send out message given a message... sendmail?'''
  pass
  
#####

# SYSTEM ADMIN functions
def create_group(n, loc):
  ''' Given a name, n, and location, loc, create a group with those attributes and save it in the database. Return the id '''
  g = Group(name=n, location=loc)
  g.save()
  return g.id
  
def delete_group(group_id):
  ''' Perhaps we should be matching with name/location instead? 
  Given a group id, remove it from the database '''
  Group.object.get(id = group_id).delete()
  
def edit_group(group_id, edit_params):
  ''' Given a group id and a dictionary of parameters to edit as edit_param,
      iterate through all the parameters of the dictionary and modified the value
      of that database entry in database. '''  
  group = Group.object.get(id = group_id)
  for param, value in edit_params:
    group.param = value

  group.save()
  
def add_new_head_office(request):
  ### TODO but maybe not... ask
  pass

def get_group(group_id):
  ''' Given a group id, get that group object in the group table '''
  group = Group.objects.get(id = group_id)
  return group
  
def get_all_groups():
  ''' Get all the groups in the system '''
  return Group.objects.all()
  
def get_GIPs():
  ''' Get all the GIPs in the system '''
  return GIP.objects.all()
    
  
def get_all_handlers(group_id):
  ''' Get all the handlers in the system '''
  return Handler.objects.all()  

#####

# GROUP functions

def add_GIP_to_group(gip_id, group_id):
  ''' Given a gip id and a group id, create a relation where the gip belongs to the group '''
  gip = GIP.objects.get(id = gip_id)
  group = GIP.objects.get(id = group_id)
  relation = GIPGroups()
  relation.gip_ref = gip
  relation.group_ref = group
  relation.save()
   
def delete_GIP_from_group(gip_id, group_id):
  GIPGroup.objects.get(gip_ref__id = gip_id, group_ref__id = group_id).delete()

def edit_location(group_id, loc):
  ''' Given location information, and a group id, update the location for 
      the group object with group id '''
  group = Group.objects.get(id = group_id)
  group.location = loc
  group.save()

def edit_description(group_id, n):
  ''' Given a description (name), update the description of the group object with
      the given group id '''
  group = Group.objects.get(id = group_id)
  group.name = n
  group.save()

def add_handler(handler, group):
  ''' Given a handler and group object, create a relation between handler and group '''
  hgr = HandlersGroups()
  hgr.handler_ref = handler
  hgr.group_ref = group
  hgr.save()

def delete_handler_from_group(handler, group):
  ''' Given a handler id and group id, remove the relation that says that the 
      handler belongs to the group. '''
  HandlerGroup.objects.get(handler_ref = handler, group_ref = group).delete()

def get_all_GIPs_from_group(group_id):
  ''' Given a group id, return all the GIPS who are associated with the handlers '''
  # extract all the gips from group
  gips_ref = GIPGroups.objects.filter(group_ref = group_id)
  
  # initialize list of gips
  gips = []

  # need to extract the gip object of that particular gip_ref
  for gip in gips_ref:
    g = gip.gip_ref
    gips.append(g)

  return gips

def get_all_handlers_from_group(group_id):
  ''' Given a group id, return all the handlers who are in the group with group_id '''
  # extract all the handlers in a particular group  
  handlers_ref = HandlersGroups.objects.filter(group_ref = group_id)

  # initialize list of handlers
  handlers = [] 
  
  # need to extract the handler object of that particular handler_ref_id
  for handler in handlers_ref:
    h = handler.handler_ref
    handlers.append(h)

  return handlers


