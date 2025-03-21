import pytest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse, reverse_lazy
from .models import Poll


pytestmark = pytest.mark.django_db


def test_registration(client):

	#почему тут reverse('registration') не работает я не понимаю!!!
	client.post('/enterpoll/users/registration/', {'username': 'Username1', 'password1': 'Helloworld1', 'password2': 'Helloworld1'}, follow=True)
	assert User.objects.filter(username='Username1')

def test_login(client):

	response = client.post(reverse('login'), {'username': 'User1', 'password': 'Helloworld1'}, follow=True)
	assert response.context['user'].is_authenticated

def test_logout(client):

	client.post(reverse('login'), {'username': 'User1', 'password': 'Helloworld1'}, follow=True)
	response = client.post(reverse('logout'), follow=True)
	assert not response.context['user'].is_authenticated

def test_delete_user(client):

	client.post(reverse('login'), {'username': 'User1', 'password': 'Helloworld1'}, follow=True)
	user = User.objects.get(username='User1')
	client.post(reverse('delete_user', kwargs={'user_pk': user.pk}), follow=True)
	assert not User.objects.filter(username='User1')

def test_password_change(client):

	client.post(reverse('login'), {'username': 'User1', 'password': 'Helloworld1'}, follow=True)
	user = User.objects.get(username='User1')
	client.post(reverse('password_change', kwargs={'user_pk': user.pk}), {'old_password': 'Helloworld1', 'new_password1': 'Helloworld2', 'new_password2': 'Helloworld2'})
	assert authenticate(username='User1', password='Helloworld2')

def test_profile(client):

	client.post(reverse('login'), {'username': 'User1', 'password': 'Helloworld1'}, follow=True)
	user = User.objects.get(username='User1')
	response = client.get(reverse('profile', kwargs={'user_pk': user.pk}), follow=True)
	assert response.status_code == 200

def test_main_page(client):

	response = client.get(reverse('main_page'), follow=True)
	assert response.status_code == 200

def test_poll_list(client):

	response = client.get(reverse('poll_list'), follow=True)
	assert response.status_code == 200

def test_random_poll_page(client):

	response = client.get(reverse('random_poll_page'), follow=True)
	assert response.status_code == 200

def test_create_poll(client):

	client.post(reverse('login'), {'username': 'User1', 'password': 'Helloworld1'}, follow=True)
	client.post(reverse('create_poll'), {'title': 'title1', 'description': 'description1', 'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '0', 'form-0-text': 'option0', 'form-1-text': 'option1', 'form-2-text': 'option2'}, follow=True)
	assert Poll.objects.filter(title='title1')
