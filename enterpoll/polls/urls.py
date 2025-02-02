from django.urls import path, include

from . import views

api_v1_patterns = [
	path("polls_list/", views.PollsListView.APIViewV1.as_view(), name="polls_list_api_v1"),
	path("main_page/", views.MainPageView.APIViewV1.as_view(), name="main_page_api_v1"),
]

urlpatterns = [
    path("api/v1/", include(api_v1_patterns)),
	path("", views.MainPageView.as_view(), name="main_page"),
	path("polls_list/", views.PollsListView.as_view(), name="polls_list"),
	path("create_poll/", views.CreatePollView.as_view(), name="create_poll"),
	path("polls/<int:poll_pk>/", views.PollPageView.as_view(), name="poll_page"),
	path("random_poll_page/", views.RandomPollPageView.as_view(), name="random_poll_page"),
]
