# import the models
from models import *
from django.db import transaction


# HANDLER functions
def get_handler(handler_id):
  ''' Given:  handler_id -      int
      Return handler django object '''
  return Handler.objects.get(id=handler_id)

def delete_gip(gip_id): 
  ''' Given:  gip_id -          int
      Return nothing. Removes the GIP django object at gip_id from database '''
  gip = GIP.objects.get(id=gip_id)
  gip.delete()  

def edit_gip(gip_id, new_data):
  ''' Do we really need this? GIP only stores registration info right now...

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

#def get_name(gip_id):
#  ''' Given: gip_id -          int
#      Return the name (as string) of the gip associated with gip_id '''
#  gip = GIP.objects.get(id=gip_id)
#  return gip.name
  
def change_password(handler_id, new_password):
  ''' Given: handler_id -     int
             new_password -   string
      Return the handler object with the password changed '''
  handler = Handler.objects.get(id = handler_id)
  handler.password = new_password
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
  
#####

# HEAD OFFICE functions
def create_admin(handler_id):
  ''' Given:  handler_id -        int
      Return a new system admin object that references object at handler_id '''
  handler = Handler.objects.get(id = handler_id)

  try:
    sys_admin = SystemAdmin(handler_ref = handler)
  # if the handler is already a system admin, just return the system admin object
  except:
    sys_admin = SystemAdmin.objects.get(handler_ref = handler)
  return sys_admin

def add_new_handler(n, loc):
  ''' Given:  n -                 string
              loc -               string
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
def create_group(n, loc):
  ''' Given a name, n, and location, loc, create a group with those attributes and save it in the database. Return the django group object '''
  g = Group(name=n, location=loc)
  g.save()
  return g
  
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

def edit_description(group_id, n):
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

def get_all_GIPs_from_group(group_id):
  ''' Given a group id, return all the GIPS who are associated with the handlers as a list'''
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
  ''' Given a group id, return all the handlers who are in the group with group_id as a list'''
  # extract all the handlers in a particular group  
  handlers_ref = HandlersGroups.objects.filter(group_ref = group_id)

  # initialize list of handlers
  handlers = [] 
  
  # need to extract the handler object of that particular handler_ref_id
  for handler in handlers_ref:
    h = handler.handler_ref
    handlers.append(h)

  return handlers


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
