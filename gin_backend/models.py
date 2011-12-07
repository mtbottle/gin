from django.db import models
from django.utils.hashcompat import md5_constructor

def encode_password(salt, raw_password):
	''' Encode the password with md5 encoding. similar to get_hexdigest in django/trunk/django/contrib/auth/models.py'''
	return md5_constructor(salt + raw_password).hexdigest()

def check_password(raw_password, hash_password):
	''' Return true if the raw_password is the same as hash_password. similar to check_password in django/trunk/django/contrib/auth/models.py '''
	algo, salt, hsh = hash_password.split('$')
	assert(algo == 'md5')
	return hsh == get_hexdigest(salt, raw_password)

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
	password = models.TextField()
	
	def __unicode__(self):
		return "Handler : (name: %s, contact_info: %s, location: %s, head_office: %d)" % \
			(self.name, self.contact_info, self.location, self.head_office)

class Group(models.Model):
	''' class of group objects '''
	name = models.CharField(max_length=100)
	location = models.TextField()

	def __unicode__(self):
		return "Group : (name: %s, location: %s)" % (self.name, self.location)

class GIP(models.Model):
	''' ground information person (?) '''
	self_register = models.IntegerField()       # 1 or 0, where 0 is False and 1 is True
		
	# For admin site 
	def __unicode__(self):
		return "GIP : (id: %d, self register: %d)" % (self.id, self.self_register)

class ContactMedium(models.Model):
	''' Information stored for contact mediums '''
	gip = models.ForeignKey(GIP)
	t = models.CharField(max_length=100)        # type, don't want to confuse with python inbuilt 'type'
	description = models.TextField()
	preferred_contact = models.IntegerField()   # ranking for how preferred this contact is (1-5 scale?)

	def __unicode__(self):
		return "Contact Medium : (gip id: %d, type: %s, description: %s)" % (self.gip, self.t, self.description)

class Message(models.Model):
	''' Class to store message and the meta-data for messages '''
	message = models.TextField()
	# this takes in the time and date it was entered, not really sent. 
	# so the time might be off if messages are in queue waiting to be entered into the database
	datetime_sent = models.DateTimeField(auto_now_add = True)
	contact_medium = models.ForeignKey(ContactMedium)
	flag = models.IntegerField()                # [unprocessed, accept, reject] 0,1,2 in order
	routing_origin = models.TextField()         # location information   

	def __unicode__(self):
		return "%s \n" % (self.message)

class Tag(models.Model):
	tag = models.CharField(max_length=100)
	description = models.TextField()

	def __unicode__(self):
		return "Tag : %s, \n%s" % (self.tag, self.description)



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
		return "This is handler tag"
 
class GroupsTag(models.Model):
	grouop_ref = models.ForeignKey(Group)
	tag_ref = models.ForeignKey(Tag)

	def __unicode__(self):
		''' TODO Find a better way to format this information '''
		return "This is group tag"
 


######## Relational Information

class HandlerFlagMessage(models.Model):
	class Meta:
		# denotes that this pair is unique, avoids multiple entries in the database
		unique_together = ['handler_ref', 'message_ref']

	handler_ref = models.ForeignKey(Handler)
	message_ref = models.ForeignKey(Message)

	def __unicode__(self):
		''' TODO Find a better way to format this information '''
		return "Handler %d belongs to group %s" % (self.handler_ref, self.group_ref)

class HandlersGroups(models.Model):
	''' Relation information between handlers and group. '''
	class Meta:
		# denotes that this pair is unique, avoids multiple entries in the database
		unique_together = ['handler_ref', 'group_ref']

	handler_ref = models.ForeignKey(Handler)
	group_ref = models.ForeignKey(Group)

	def __unicode__(self):
		''' TODO Find a better way to format this information '''
		return "Handler %d belongs to group %s" % (self.handler_ref, self.group_ref)

class GIPGroups(models.Model):
	''' Relation information between GIP and groups '''
	class Meta:
		# denotes that this pair is unique, avoids multiple entries in the database
		unique_together = ['gip_ref', 'group_ref']
	gip_ref = models.ForeignKey(GIP)
	group_ref = models.ForeignKey(Group)

	def __unicode__(self):
		''' TODO Find a better way to format this information '''
		return "GIP %d belongs to group %d" % (self.gip_ref, self.group_ref)

class SystemAdmin(models.Model):
	''' Specifies which handler is a system admin. There can only be one... per handler '''
	handler_ref = models.OneToOneField(Handler)

	def __unicode__(self):
		''' TODO Find a better way to format this information '''
		return "Handler %d is a system admin" % (self.handler_ref_id)
