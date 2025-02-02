from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import modelformset_factory
from django.forms.models import model_to_dict
from polls.forms import PollModelForm, CommentModelForm
from polls.models import Poll, Choice, Vote, Rating, Comment
from django.core.paginator import Paginator
import random

from rest_framework import (
	views as rest_views,
	generics as rest_generics,
	response as rest_response
)
from .serializers import PollsListSerializer

# Create your views here.

class MainPageView(TemplateView):

	template_name = 'polls/main_page.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		polls = Poll.objects.all()
		context['most_popular_polls'] = sorted(polls, key=Poll.get_number_of_votes, reverse=True)[0:3]
		context['highly_rated_polls'] = sorted(polls, key=Poll.get_average_rating, reverse=True)[0:3]
		context['latest_polls'] = polls.order_by('-created')[0:3]
		return context

	class APIViewV1(rest_views.APIView):

		def get(self, request):
			polls = Poll.objects.all()
			most_popular_polls = sorted(polls, key=Poll.get_number_of_votes, reverse=True)[0:3]
			highly_rated_polls = sorted(polls, key=Poll.get_average_rating, reverse=True)[0:3]
			latest_polls = polls.order_by('-created')[0:3]
			response_dict = {
				'most_popular_polls_id': [poll.id for poll in most_popular_polls],
				'highly_rated_polls_id': [poll.id for poll in highly_rated_polls],
				'latest_polls_id': [poll.id for poll in latest_polls]
			}
			return rest_response.Response(response_dict)

class PollsListView(ListView):

	model = Poll
	ordering = '-created'
	paginate_by = 10
	page_kwarg = 'page_number'
	context_object_name = 'polls'
	template_name = 'polls/polls_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_kwarg'] = self.page_kwarg
		return context

	class APIViewV1(rest_generics.ListAPIView):

		queryset = Poll.objects.all()
		serializer_class = PollsListSerializer

class CreatePollView(LoginRequiredMixin, TemplateView):

	template_name = 'polls/create_poll.html'
	min_choices_number = 2

	def get(self, request, *args, **kwargs):
		choice_modelformset = self._get_choice_modelformset(request)
		return render(
			request,
			self.template_name,
			context={
				'poll_modelform': PollModelForm(),
				'choice_modelformset': choice_modelformset
			}
		)

	def post(self, request, *args, **kwargs):
		poll_modelform = PollModelForm(request.POST)
		choice_modelformset = self._get_choice_modelformset(request)
		if poll_modelform.is_valid() and choice_modelformset.is_valid():
			poll = poll_modelform.save(commit=False)
			poll.user = request.user
			poll.save()
			choices = choice_modelformset.save(commit=False)
			for choice in choices:
				choice.poll = poll
				choice.save()
			return redirect(poll)
		else:
			return render(
				request,
				self.template_name,
				context={
					'poll_modelform': poll_modelform,
					'choice_modelformset': choice_modelformset
				}
			)

	def _get_choice_modelformset(self, request):
		choice_modelformset_class = modelformset_factory(
			Choice,
			fields=['text'],
			extra=self._get_choices_number(request),
			widgets={'text': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'required': True})}
		)
		if request.method == "POST":
			return choice_modelformset_class(request.POST)
		else:
			return choice_modelformset_class(queryset=Choice.objects.none())

	def _get_choices_number(self, request):
		if request.method == "GET":
			return int(request.GET.get('choices_number', self.min_choices_number))
		elif request.method == "POST":
			return int(request.POST['form-TOTAL_FORMS'])
		else:
			return 2

class RandomPollPageView(RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		pk_list = Poll.objects.values_list('pk', flat=True)
		return reverse('poll_page', kwargs={'poll_pk': random.choice(pk_list)})

class PollPageView(TemplateView):

	paginate_by = 5
	template_name = 'polls/poll_page.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['poll'] = get_object_or_404(Poll, pk=self.kwargs['poll_pk'])
		if self.request.user.is_authenticated:
			try:
				context['user_choice'] = Vote.objects.get(user=self.request.user, poll=context['poll']).choice
			except Vote.DoesNotExist:
				pass
			try:
				context['user_rating'] = Rating.objects.get(user=self.request.user, poll=context['poll'])
			except Rating.DoesNotExist:
				pass
		context['comments'] = Comment.objects.filter(poll=context['poll']).order_by('-created')
		comments_paginator = Paginator(context['comments'], self.paginate_by)
		context['comments_page_kwarg'] = 'comments_page_number'
		context['comments_page_number'] = self.request.GET.get(context['comments_page_kwarg'])
		context['comments_page_obj'] = comments_paginator.get_page(context['comments_page_number'])
		context['comment_modelform'] = CommentModelForm()
		return context

	def post(self, request, *args, **kwargs):
		poll_pk = kwargs['poll_pk']
		match request.POST['action_type']:
			case 'delete_poll': return delete_poll(request, poll_pk)
			case 'vote': return vote(request, poll_pk)
			case 'delete_vote': return delete_vote(request, poll_pk)
			case 'rate': return rate(request, poll_pk)
			case 'delete_rating': return delete_rating(request, poll_pk)
			case 'comment':
				result = comment(request, poll_pk)
				if isinstance(result, HttpResponseRedirect):
					return result
				elif isinstance(result, CommentModelForm):
					context = self.get_context_data(*args, **kwargs)
					context['comment_modelform'] = result
					return render(request, self.template_name, context)
			case 'delete_comment': return delete_comment(request, poll_pk)

@login_required
def delete_poll(request, poll_pk):
	Poll.objects.get(pk=poll_pk).delete()
	return redirect('main_page')

@login_required
def vote(request, poll_pk):
	user = request.user
	poll = Poll.objects.get(pk=poll_pk)
	choice = poll.choice_set.get(pk=request.POST['choice_pk'])
	try:
		vote = Vote.objects.get(user=user, poll=poll)
		vote.choice = choice
		vote.save()
	except:
		Vote.objects.create(user=request.user, poll=poll, choice=choice)
	return redirect(poll)

@login_required
def delete_vote(request, poll_pk):
	user = request.user
	poll = Poll.objects.get(pk=poll_pk)
	Vote.objects.get(user=request.user, poll=poll).delete()
	return redirect(poll)

@login_required
def rate(request, poll_pk):
	user = request.user
	poll = Poll.objects.get(pk=poll_pk)
	rating_value = request.POST['rating_value']
	try:
		rating = Rating.objects.get(user=user, poll=poll)
		rating.value = rating_value
		rating.save()
	except:
		Rating.objects.create(user=user, poll=poll, value=rating_value)
	return redirect(poll)

@login_required
def delete_rating(request, poll_pk):
	user = request.user
	poll = Poll.objects.get(pk=poll_pk)
	Rating.objects.get(user=user, poll=poll).delete()
	return redirect(poll)

@login_required
def comment(request, poll_pk):
	user = request.user
	poll = Poll.objects.get(pk=poll_pk)
	comment_modelform = CommentModelForm(request.POST)
	if comment_modelform.is_valid():
		comment_text = comment_modelform.cleaned_data['text']
		Comment.objects.create(user=user, poll=poll, text=comment_text)
		return redirect(poll)
	else:
		return comment_modelform

@login_required
def delete_comment(request, poll_pk):
	poll = Poll.objects.get(pk=poll_pk)
	Comment.objects.get(pk=request.POST['comment_pk']).delete()
	return redirect(poll)
