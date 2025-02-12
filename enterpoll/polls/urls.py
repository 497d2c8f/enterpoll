from django.urls import path
from . import views, api_views


urlpatterns = [
	path("", views.MainPageView.as_view(), name="main_page"),
	path("polls/list/", views.PollsListView.as_view(), name="polls_list"),
	path("polls/create/", views.CreatePollView.as_view(), name="create_poll"),
	path("polls/<int:poll_pk>/", views.PollPageView.as_view(), name="poll_page"),
	path("polls/random/", views.RandomPollPageView.as_view(), name="random_poll_page"),
]
