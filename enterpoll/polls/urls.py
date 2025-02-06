from django.urls import path, include

from . import views, api_views

api_v1_patterns = [
	path("main_page/", api_views.MainPageAPIViewV1.as_view(), name="main_page_api_v1"),
	path("polls/list/", api_views.PollListAPIViewV1.as_view(), name="poll_list_api_v1"),
	path("polls/create/", api_views.CreatePollAPIViewV1.as_view(), name="create_poll_api_v1"),
	path("polls/<int:poll_pk>/", api_views.DetailedPollAPIViewV1.as_view(), name="detailed_poll_api_v1"),
	path("polls/<int:poll_pk>/delete/", api_views.DeletePollAPIViewV1.as_view(), name="delete_poll_api_v1"),
	path("polls/<int:poll_pk>/comment_list/", api_views.PollCommentListAPIViewV1.as_view(), name="poll_comment_list_api_v1"),
	path("polls/<int:poll_pk>/create_comment/", api_views.CreatePollCommentAPIViewV1.as_view(), name="create_comment_api_v1"),
	path("comments/<int:comment_pk>/", api_views.CommentAPIViewV1.as_view(), name="comment_api_v1"),
	path("comments/<int:comment_pk>/delete/", api_views.DeleteCommentAPIViewV1.as_view(), name="delete_comment_api_v1"),
]

urlpatterns = [
    path("api/v1/", include(api_v1_patterns)),
	path("", views.MainPageView.as_view(), name="main_page"),
	path("polls/list/", views.PollsListView.as_view(), name="polls_list"),
	path("polls/create/", views.CreatePollView.as_view(), name="create_poll"),
	path("polls/<int:poll_pk>/", views.PollPageView.as_view(), name="poll_page"),
	path("polls/random/", views.RandomPollPageView.as_view(), name="random_poll_page"),
]
