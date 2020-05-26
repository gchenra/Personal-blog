import math
from django.db import models
from django.utils.text import Truncator

# import the auth module for user class
from django.contrib.auth.models import User 
from django.utils.html import mark_safe
from markdown import markdown

# each class is subclass of django.db.models.Model class
# each field of each class is an instance of django.db.models.Field class
# there are other fields such as IntegerField, BooleanField, and DecimalField
# pretty much like MySQL database types. 
class Board(models.Model):
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	def get_posts_count(self):
		return Post.objects.filter(topic__board=self).count()

	def get_last_post(self):
		return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
	subject = models.CharField(max_length=255)
	last_update = models.DateTimeField(auto_now_add=True)
	# add foreignkey field tell django that any one Topic inrance 
	# is only realted to one Board instance. 
	# the related_name parameter will be used to create a reverse
	# relationship where the Board instance will have access to a list
	# of Topics instances that belong to that Board. 

	# for Django 3.0.5, the ForeignKey field has two positional arguments:
	# 1. the class this foreignkey is referring to 
	# 2. on_delete = what to do, detail see on the website below
	# https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ForeignKey.on_delete
	board = models.ForeignKey(Board, models.DO_NOTHING, related_name='topics')
	starter = models.ForeignKey(User, models.DO_NOTHING, related_name='topics')
	views = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.subject

	def get_page_count(self):
		count = self.posts.count()
		pages = count / 20
		return math.ceil(pages)

	def has_many_pages(self, count=None):
		if count is None:
			count = self.get_page_count()
		return count > 6

	def get_page_range(self):
		count = self.get_page_count()
		if self.has_many_pages(count):
			return range(1, 5)
		return range(1, count + 1)

	def get_last_ten_posts(self):
		return self.posts.order_by('-created_at')[:10]

class Post(models.Model):
	message = models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic, models.DO_NOTHING, related_name='posts')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='posts')
	# related_name = '+' means don't create the reverse relationship
	updated_by = models.ForeignKey(User, models.DO_NOTHING, null=True ,related_name='+')

	def __str__(self):
		truncated_message = Truncator(self.message)
		return truncated_message.chars(30)

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message, safe_mode='escape'))














