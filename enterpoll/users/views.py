from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import auth
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import custom_validators

# Create your views here.

class RegistrationView(CreateView):

	form_class = UserCreationForm
	template_name = 'users/registration.html'
	success_url = reverse_lazy('login')

#	def clean(self):
#		cleaned_data = self.cleaned_data
#		print(cleaned_data)
#		custom_validators.forbidden_words(cleaned_data['username'])
#		return cleaned_data
#
#	def get_form_class(self):
#		form_class = super().get_form_class()
#		form_class.clean = self.clean
#		return form_class

class DeleteView(DeleteView):

	model = User
	pk_url_kwarg = 'user_pk'
	template_name = 'users/delete_user.html'
	success_url = reverse_lazy('main_page')
	
class LoginView(LoginView):

	template_name = 'users/login.html'
	next_page = reverse_lazy('polls_list')

def logout(request):

	auth.logout(request)
	return redirect('login')

class ProfileView(DetailView):

	model = User
	pk_url_kwarg = 'user_pk'
	paginate_by = 5
	template_name = 'users/profile.html'

	def get_context_data(self, *args, **kwargs):

		context = super().get_context_data(*args, **kwargs)

		context['user_polls'] = self.request.user.poll_set.order_by('-created')
		user_polls_paginator = Paginator(context['user_polls'], self.paginate_by)
		context['user_polls_page_kwarg'] = 'user_polls_page_number'
		context['user_polls_page_number'] = self.request.GET.get(context['user_polls_page_kwarg'])
		context['user_polls_page_obj'] = user_polls_paginator.get_page(context['user_polls_page_number'])

		context['user_votes'] = self.request.user.vote_set.order_by('-created')
		user_votes_paginator = Paginator(context['user_votes'], self.paginate_by)
		context['user_votes_page_kwarg'] = 'user_votes_page_number'
		context['user_votes_page_number'] = self.request.GET.get(context['user_votes_page_kwarg'])
		context['user_votes_page_obj'] = user_votes_paginator.get_page(context['user_votes_page_number'])

		context['user_ratings'] = self.request.user.rating_set.order_by('-value')
		user_ratings_paginator = Paginator(context['user_ratings'], self.paginate_by)
		context['user_ratings_page_kwarg'] = 'user_ratings_page_number'
		context['user_ratings_page_number'] = self.request.GET.get(context['user_ratings_page_kwarg'])
		context['user_ratings_page_obj'] = user_ratings_paginator.get_page(context['user_ratings_page_number'])

		context['user_comments'] = self.request.user.comment_set.order_by('-created')
		user_comments_paginator = Paginator(context['user_comments'], self.paginate_by)
		context['user_comments_page_kwarg'] = 'user_comments_page_number'
		context['user_comments_page_number'] = self.request.GET.get(context['user_comments_page_kwarg'])
		context['user_comments_page_obj'] = user_comments_paginator.get_page(context['user_comments_page_number'])

		return context

class PasswordChangeView(PasswordChangeView):

	template_name = 'users/password_change.html'

	def get_success_url(self, *args, **kwargs):
		return reverse('password_change_done', kwargs={'user_pk': self.kwargs['user_pk']})

class PasswordChangeDoneView(PasswordChangeDoneView):

	template_name = 'users/password_change_done.html'
