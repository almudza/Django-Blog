from django.db import models

# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from markdown_deux import markdown

from django.utils.safestring import mark_safe

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')

def upload_location(objects, filename):
	# filebase, extension = filename.split(".")
	# return "%s/%s.%s" %(instance.id, instance.id, extension)
	return "%s/%s" %(objects.id, filename)


class Post(models.Model):
	STATUS_CHOICES = (
			('draft', 'Draft'),
			('published', 'Published'),

		)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, related_name='blog_posts')
	body = models.TextField()
	image = models.ImageField(upload_to=upload_location,
			null=True,
			blank=True, 
			width_field= "width_field",
			height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	objects = models.Manager()#the default Manager
	published = PublishedManager() # Our custom manager
	tags = TaggableManager()


	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail',
					args=[self.publish.year,
						self.publish.strftime('%m'),
						self.publish.strftime('%d'),
						self.slug])

	def get_markdown(self):
		body = self.body
		markdown_text = markdown(body)
		return mark_safe(markdown_text)



class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)


	class Meta:
		ordering = ('created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)