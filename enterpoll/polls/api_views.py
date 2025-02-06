from django.utils.translation import gettext_lazy as _
from polls.models import Poll, Choice, Comment
from .api_serializers import (
	PollListSerializer,
	PollAndChoicesSerializer,
	DetailedPollSerializer,
	CommentListSerializer,
	CommentSerializer,
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

	queryset = Poll.objects.all()
	serializer_class = PollListSerializer

class CreatePollAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = PollAndChoicesSerializer

	def create(self, request, *args, **kwargs):
		response = super().create(request, *args, **kwargs)
		response.data = DetailedPollSerializer(Poll.objects.get(**request.data['poll'])).data
		return response

class DetailedPollAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Poll.objects.all()
	serializer_class = DetailedPollSerializer
	lookup_url_kwarg = 'poll_pk'

#	def retrieve(self, request, *args, **kwargs):
#		poll = self.queryset.get(pk=kwargs[self.lookup_url_kwarg])
#		serializer = self.serializer_class(poll)
#		return drf_response.Response(serializer.data)

class DeletePollAPIViewV1(drf_generics.DestroyAPIView):

	queryset = Poll.objects.all()
	lookup_url_kwarg = 'poll_pk'

class PollCommentListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = CommentListSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.comment_set.all()
		return queryset

class CreatePollCommentAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = CommentSerializer

class CommentAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'

class DeleteCommentAPIViewV1(drf_generics.DestroyAPIView):

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'
