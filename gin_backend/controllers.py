# import the models
from models import *
from django.db import transaction


# HANDLER functions
def delete_GIP(request):
  pass
  
def edit_GIP(request):
  pass
  
def get_name(request):
  pass
  
def change_password(request):
  pass
  
def change_location(request):
  pass

def add_new_GIP(request):
  pass
  
#####

# HEAD OFFICE functions
def add_new_handler(request):
  pass
  
def delete_handler(request):
  pass
  
def move_handler_to_group(request):
  pass
  
def message_group_handlers(request):
  pass
  
def new_operation(request):
  pass
  
#####

# SYSTEM ADMIN functions
def create_group(request):
  pass
  
def delete_group(request):
  pass
  
def edit_group(request):
  pass
  
def add_new_head_office(request):
  pass

def get_group(request, group_id):
  group = Group.objects.get(id = group_id)
  return group
  
def get_all_groups(request):
  return Group.objects
  
def get_GIPs(request):
  pass
  
def get_all_handlers(request):
  pass
  
#####

# 
