from django.db import models

# Create your models here.
class Handler(models.Model):
  ''' class of handler objects '''
  name = models.CharField(max_length=100)
  # contact and location info can be abstracted into another level as well... but let's just leave it as plain text for now
  contact_info = models.TextField()
  location = models.TextField()
  # to differentiate whether or not a handler is part of head office
  # system admin is differentiated with their own table of foreign key references
  head_office = models.BooleanField()
  
  def __unicode__(self):
    return name

class Group(models.Model):
  ''' class of group objects '''
  name = models.CharField(max_length=100)
  location = models.TextField()

  def __unicode__(self):
    return name


class GIP(models.Model):
  ''' ground information person (?) '''
  self_register = models.IntegerField()       # 1 or 0, where 0 is False and 1 is True
    
  # For admin site 
  def __unicode__(self):
    return self.id
   

class ContactMedium(models.Model):
  ''' Information stored for contact mediums '''
  gip = models.ForeignKey(GIP)
  t = models.CharField(max_length=100)        # type, don't want to confuse with python inbuilt 'type'
  description = models.TextField()
  preferred_contact = models.IntegerField()   # ranking for how preferred this contact is (1-5 scale?)

  def __unicode__(self):
    return self.t 

class Message(models.Model):
  ''' Class to store message and the meta-data for messages '''
  gip = models.ForeignKey(GIP)
  message = models.TextField()
  # this takes in the time and date it was entered, not really sent. 
  # so the time might be off if messages are in queue waiting to be entered into the database
  datetime_sent = models.DateTimeField(auto_now_add = True)
  contact_medium = models.ForeignKey(ContactMedium)
  flag = models.IntegerField()                # [unprocessed, accept, reject] 0,1,2 in order
  routing_origin = models.CharField()         # location information   

  def __unicode__(self):
    return message

class Tag(models.Model):
  tag = models.CharField(max_length=100)
  description = models.TextField()

  def __unicode__(self):
    return tag



######## Relational Tag information

class MessageTag(models.Model):
  message_ref = models.ForeignKey(Message)
  tag_ref = models.ForeignKey(Tag)

  def __unicode__(self):
    ''' TODO Find a better way to format this information '''
    return "This is message tag"
  
class GIPTag(models.Model):
  gip_ref = models.ForeignKey(GIP)
  tag_ref = models.ForeignKey(Tag)

  def __unicode__(self):
    ''' TODO Find a better way to format this information '''
    return "This is GIP tag"
  
class HandlersTag(models.Model):
  handler_ref = models.ForeignKey(Handler)
  tag_ref = models.ForeignKey(Tag)

  def __unicode__(self):
    ''' TODO Find a better way to format this information '''
    return "This is GIP tag"
 
class GroupsTag(models.Model):
  grouop_ref = models.ForeignKey(Group)
  tag_ref = models.ForeignKey(Tag)

  def __unicode__(self):
    ''' TODO Find a better way to format this information '''
    return "This is GIP tag"
 


######## Relational Information

class HandlersGroups(models.Model):
  handler_ref = models.ForeignKey(Handler)
  group_ref = models.ForeignKey(Group)

  def __unicode__(self):
    ''' TODO Find a better way to format this information '''
    return "This is a Handler-Group relation"

class SystemAdmin(models.Model):
  handler_ref = models.ForeignKey(Handler)

  def __unicode__(self):
    ''' TODO Find a better way to format this information '''
    return "This is a System Admin relation"
