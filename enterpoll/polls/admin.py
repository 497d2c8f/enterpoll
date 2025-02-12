from django.contrib import admin
from .models import Poll, Choice, Comment
from django import forms

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

	list_display = ['title', 'user', 'created', 'average_rating']
	fields = [
		'title',
		'description',
		'choices',
		'user',
		(
			'created',
			'number_of_votes',
			'average_rating'
		)
	]
	readonly_fields = [
		'title',
		'description',
		'choices',
		'user',
		'created',
		'number_of_votes',
		'average_rating',
	]
	search_fields = ['title', 'description', 'user__username']
	search_help_text = 'Поиск по заголовку, описанию или автору.'
	list_filter = ['created']
	list_per_page = 10
	list_max_show_all = 100
	ordering = ['-created']
	show_facets = admin.ShowFacets.ALWAYS
	has_add_permission = lambda *args: False
	has_change_permission = lambda *args: False

	@admin.display(description='Варианты ответа (количество голосов)')
	def choices(self, instance):
		choices_and_votes = sorted(
			(
				(c.text, c.number_of_votes) for c in instance.choice_set.all()
			),
			key=lambda item: item[1],
			reverse=True
		)
		text = '\n'.join(f'{c} ({v})' for c, v in choices_and_votes)
		return text
	
#	@admin.display(description='Количество голосов')
#	def number_of_votes(self, instance):
#		return instance.number_of_votes
	
	@admin.display(description='Рейтинг')
	def average_rating(self, instance):
		return round(instance.average_rating, 2)
