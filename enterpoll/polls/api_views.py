from django.utils.translation import gettext_lazy as _
from polls.models import Poll, Choice
from .api_serializers import PollsListSerializer, CreatePollSerializer
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

class CreatePollAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = CreatePollSerializer

	def post(self, request, *args, **kwargs):
		user_polls = Poll.objects.filter(user=request.user)
		if not user_polls or user_polls.last().is_published:
			return super().post(request, *args, **kwargs)
		number_of_choices = user_polls.last().get_number_of_choices()
		if number_of_choices < 2:
			raise drf_exceptions.APIException(detail=_(f'User ({request.user.username}) has unpublished poll (pk = {user_polls.last().pk}) with an unacceptable number of choices ({number_of_choices}, but it requires 2-10 choices).'))

	def perform_create(self, serializer):
		'''
		Метод perform_create из rest_framework.mixins.CreateModelMixin.
		Метод save сериализатора принимает дополнительные ключевые аргументы,
		которые в итоге передаются методу создания объекта модели Poll.
		Теперь текущий пользователь автоматически становится автором создаваемого опроса.
		ЭТИ ДВЕ СТРОКИ СТОИЛИ МНЕ НЕСКОЛЬКИХ ЧАСОВ ЧТЕНИЯ КОДА DJANGO REST FRAMEWORK!!!
		ГОРЖУСЬ ЭТИМИ СТРОКАМИ!!!
		'''
		serializer.save(user=self.request.user, is_published=False)

class CreateChoiceAPIViewV1(drf_generics.CreateAPIView): pass
