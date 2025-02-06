from django.utils.translation import gettext_lazy as _
from polls.models import Poll, Choice, Vote, Comment
from .api_serializers import (
	PollSerializer,
	CommentSerializer,
	VoteSerializer,
	ChoiceSerializer
)
from rest_framework import (
	status,
	exceptions as drf_exceptions,
	views as drf_views,
	generics as drf_generics,
	response as drf_response
)




class MainPageAPIViewV1(drf_views.APIView):

	def get(self, request):
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

	serializer_class = PollSerializer

class GetPollAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Poll.objects.all()
	serializer_class = PollSerializer
	lookup_url_kwarg = 'poll_pk'

class DeletePollAPIViewV1(drf_generics.DestroyAPIView):

	queryset = Poll.objects.all()
	lookup_url_kwarg = 'poll_pk'




class VoteListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = VoteSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.vote_set.order_by('-created')
		return queryset

class CreateVoteAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = VoteSerializer

class GetVoteAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
	lookup_url_kwarg = 'vote_pk'

class DeleteVoteAPIViewV1(drf_generics.DestroyAPIView):

	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
	lookup_url_kwarg = 'vote_pk'




class CommentListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = CommentSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.comment_set.order_by('-created')
		return queryset

class CreatePollCommentAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = CommentSerializer

class GetCommentAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'

class DeleteCommentAPIViewV1(drf_generics.DestroyAPIView):

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'
