from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import (
	views as drf_views,
	response as drf_response
)


class LoginAPIViewV1(drf_views.APIView):

	def post(self, request, *args, **kwargs):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		print(request.user)
		if user is not None:
			login(request, user)
		print(request.session.session_key, request.META['CSRF_COOKIE'])
		response_dict = {'session_key': request.session.session_key, 'csrftoken': request.META['CSRF_COOKIE']}
		return drf_response.Response(response_dict)
