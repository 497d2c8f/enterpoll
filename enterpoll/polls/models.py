from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib import admin
import custom_validators

# Create your models here.

class Poll(models.Model):

	title = models.CharField('Заголовок', max_length=100, validators=[custom_validators.forbidden_words])
	description = models.CharField('Описание', max_length=100, blank=True, validators=[custom_validators.forbidden_words])
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
	created = models.DateTimeField('Время создания', auto_now_add=True)

	def __str__(self):
		length = 50
		return self.title if len(self.title) < length else self.title[:length] + '…'

	def get_absolute_url(self):
		return reverse('poll_page', kwargs={"poll_pk": self.pk})

	def get_number_of_votes(self):
		return self.vote_set.count()

	def get_number_of_comments(self):
		return self.comment_set.count()

	def get_number_of_ratings(self):
		return self.rating_set.count()

	def get_average_rating(self):
		return self.rating_set.aggregate(Avg('value', default=0))['value__avg']

class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE, blank=True)
	text = models.CharField('', max_length=100, validators=[custom_validators.forbidden_words])

	def __str__(self):
		length = 50
		return self.text if len(self.text) < length else self.text[:length] + '…'

	def get_number_of_votes(self):
		return self.vote_set.count()

class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now=True)

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	value = models.IntegerField()
	created = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	text = models.CharField('Текст', max_length=100, validators=[custom_validators.forbidden_words])
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		length = 50
		return self.text if len(self.text) < length else self.text[:length] + '…'
