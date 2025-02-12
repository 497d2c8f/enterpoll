from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from .api_permissions import IsUserOrAdmin, IsUserOnly
from rest_framework import (
	views as drf_views,
	generics as drf_generics,
	response as drf_response,
)
from .api_serializers import (
	UserSerializer
)
from polls.api_serializers import (
	PollSerializer,
	VoteSerializer,
	RatingSerializer,
	CommentSerializer
)


class RegistrationAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = UserSerializer

class ProfileAPIViewV1(drf_generics.RetrieveAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = UserSerializer
	lookup_url_kwarg = 'user_pk'
	queryset = User.objects.all()

class UserPollListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = PollSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.poll_set.order_by('-created')
		return queryset

class UserVoteListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = VoteSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.vote_set.order_by('-created')
		return queryset

class UserRatingListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = RatingSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.rating_set.order_by('-created')
		return queryset

class UserCommentListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = CommentSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.comment_set.order_by('-created')
		return queryset


class DeleteAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = UserSerializer
	lookup_url_kwarg = 'user_pk'
	queryset = User.objects.all()

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

class PasswordChangeAPIViewV1(drf_generics.UpdateAPIView):

	permission_classes = [IsUserOnly]
	serializer_class = UserSerializer
	lookup_url_kwarg = 'user_pk'
	queryset = User.objects.all()

	def partial_update(self, request, *args, **kwargs):
		validate_password(request.data['new_password'])
		requested_user = self.get_object()
		authenticated_user = authenticate(username=requested_user.username, password=request.data['current_password'])
		if authenticated_user:
			authenticated_user.set_password(request.data['new_password'])
			authenticated_user.save()
		serializer = self.get_serializer(authenticated_user)
		return drf_response.Response({'message': 'Password successfully changed.', **serializer.data})
