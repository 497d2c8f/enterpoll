from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from polls.models import Poll, Choice, Vote, Comment, Rating
from rest_framework import permissions
from .api_permissions import IsAuthorOrAdmin
from .api_serializers import (
	PollSerializer,
	CommentSerializer,
	VoteSerializer,
	RatingSerializer,
	ChoiceSerializer
)
from rest_framework import (
	views as drf_views,
	generics as drf_generics,
	response as drf_response,
	permissions as drf_permissions
)
import random




class MainPageAPIViewV1(drf_views.APIView):

	def get(self, request, *args, **kwargs):
		polls = Poll.objects.all()
		most_popular_polls = sorted(polls, key=Poll.get_number_of_votes, reverse=True)[0:3]
		highly_rated_polls = sorted(polls, key=Poll.get_average_rating, reverse=True)[0:3]
		latest_polls = polls.order_by('-created')[0:3]
		response_dict = {
			'most_popular_polls_pk': [poll.pk for poll in most_popular_polls],
			'highly_rated_polls_pk': [poll.pk for poll in highly_rated_polls],
			'latest_polls_pk': [poll.pk for poll in latest_polls]
		}
		return drf_response.Response(response_dict)




class PollListAPIViewV1(drf_generics.ListAPIView):

	queryset = Poll.objects.order_by('-created')
	serializer_class = PollSerializer

class CreatePollAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = PollSerializer

class GetPollAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Poll.objects.all()
	serializer_class = PollSerializer
	lookup_url_kwarg = 'poll_pk'

class GetRandomPollAPIViewV1(drf_views.APIView):

	def get(self, request, *args, **kwargs):
		poll_pk_list = Poll.objects.values_list('pk', flat=True)
		poll = get_object_or_404(Poll, pk=random.choice(poll_pk_list))
		serializer = PollSerializer(poll)
		return drf_response.Response(serializer.data)

class DeletePollAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]

	queryset = Poll.objects.all()
	lookup_url_kwarg = 'poll_pk'




class VoteListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = VoteSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.vote_set.order_by('-created')
		return queryset

class CreateVoteAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = VoteSerializer

class GetVoteAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
	lookup_url_kwarg = 'vote_pk'

class DeleteVoteAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]

	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
	lookup_url_kwarg = 'vote_pk'




class RatingListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = RatingSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.rating_set.order_by('-created')
		return queryset

class CreateRatingAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = RatingSerializer

class GetRatingAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Rating.objects.all()
	serializer_class = RatingSerializer
	lookup_url_kwarg = 'rating_pk'

class DeleteRatingAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]
	queryset = Rating.objects.all()
	serializer_class = RatingSerializer
	lookup_url_kwarg = 'rating_pk'




class CommentListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = CommentSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.comment_set.order_by('-created')
		return queryset

class CreatePollCommentAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = CommentSerializer

class GetCommentAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'

class DeleteCommentAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'
