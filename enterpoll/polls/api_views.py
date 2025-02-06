from django.utils.translation import gettext_lazy as _
from polls.models import Poll, Choice
from .api_serializers import PollsListSerializer, CompletePollSerializer
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

class PollsListAPIViewV1(drf_generics.ListAPIView):

	queryset = Poll.objects.all()
	serializer_class = PollsListSerializer

class CreateCompletePollAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = CompletePollSerializer

	def get(self, *args, **kwargs):
		response_dict = {
			'complete_poll_creation_form': {
				'poll': {
					'title': '',
					'description': ''

				},
				'choices': [
					{'text': ''},
					{'text': ''}
				]
			}
		}
		return drf_response.Response(response_dict)

class DeleteCompletePollAPIViewV1(drf_generics.CreateAPIView): pass

#классы для создания/удаления голоса, оценки и комментария
