from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import (
	views as drf_views,
	response as drf_response
)


class LoginAPIViewV1(drf_views.APIView):

	def post(self, request, *args, **kwargs):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
		response_dict = {'session_key': request.session.session_key, 'X-CSRFTOKEN': request.META['CSRF_COOKIE']}
		return drf_response.Response(response_dict)

class LogoutAPIViewV1(drf_views.APIView):

	def post(self, request, *args, **kwargs):
		logout(request)
		message = 'Failed logout.' if request.user.is_authenticated else 'Successful logout.'
		return drf_response.Response({'message': message})
