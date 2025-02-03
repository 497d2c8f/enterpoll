from polls.models import Poll
from .api_serializers import PollsListSerializer, CreatePollSerializer
from rest_framework import (
	status,
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

class CreatePollAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = CreatePollSerializer

	#Это метод из rest_framework.mixins.CreateModelMixin
	#метод save сериализатора принимает дополнительные ключевые аргументы, которые в итоге передаются функции создания объекта модели Poll
	#теперь текущий пользователь автоматически устанавливается в создаваемом опросе
	#ЭТИ ДВЕ СТРОКИ СТОИЛИ МНЕ НЕСКОЛЬКИХ ЧАСОВ ЧТЕНИЯ КОДА DJANGO REST FRAMEWORK!!! ГОРЖУСЬ ЭТИМИ СТРОКАМИ!!!

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class CreateChoiceAPIViewV1(drf_generics.CreateAPIView): pass
