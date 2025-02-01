from django.urls import path

from . import views

urlpatterns = [
	path("", views.MainPageView.as_view(), name="main_page"),
	path("polls_list/", views.PollsListView.as_view(), name="polls_list"),
	path("create_poll/", views.CreatePollView.as_view(), name="create_poll"),
	path("polls/<int:poll_pk>/", views.PollPageView.as_view(), name="poll_page"),
	path("random_poll_page/", views.RandomPollPageView.as_view(), name="random_poll_page"),
]
