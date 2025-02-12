from django.urls import path

from . import api_views

urlpatterns = [
	path("main_page/", api_views.MainPageAPIViewV1.as_view(), name="main_page_api_v1"),

	path("polls/list/", api_views.PollListAPIViewV1.as_view(), name="poll_list_api_v1"),
	path("polls/create/", api_views.CreatePollAPIViewV1.as_view(), name="create_poll_api_v1"),
	path("polls/<int:poll_pk>/", api_views.GetPollAPIViewV1.as_view(), name="get_poll_api_v1"),
	path("polls/random/", api_views.GetRandomPollAPIViewV1.as_view(), name="get_random_poll_api_v1"),
	path("polls/<int:poll_pk>/delete/", api_views.DeletePollAPIViewV1.as_view(), name="delete_poll_api_v1"),

	path("polls/<int:poll_pk>/vote_list/", api_views.VoteListAPIViewV1.as_view(), name="vote_list_api_v1"),
	path("polls/<int:poll_pk>/vote/", api_views.CreateVoteAPIViewV1.as_view(), name="create_vote_api_v1"),
	path("votes/<int:vote_pk>/", api_views.GetVoteAPIViewV1.as_view(), name="get_vote_api_v1"),
	path("votes/<int:vote_pk>/delete/", api_views.DeleteVoteAPIViewV1.as_view(), name="delete_vote_api_v1"),

	path("polls/<int:poll_pk>/rating_list/", api_views.RatingListAPIViewV1.as_view(), name="rating_list_api_v1"),
	path("polls/<int:poll_pk>/rate/", api_views.CreateRatingAPIViewV1.as_view(), name="create_rating_api_v1"),
	path("ratings/<int:rating_pk>/", api_views.GetRatingAPIViewV1.as_view(), name="get_rating_api_v1"),
	path("ratings/<int:rating_pk>/delete/", api_views.DeleteRatingAPIViewV1.as_view(), name="delete_rating_api_v1"),

	path("polls/<int:poll_pk>/comment_list/", api_views.CommentListAPIViewV1.as_view(), name="comment_list_api_v1"),
	path("polls/<int:poll_pk>/comment/", api_views.CreatePollCommentAPIViewV1.as_view(), name="create_comment_api_v1"),
	path("comments/<int:comment_pk>/", api_views.GetCommentAPIViewV1.as_view(), name="get_comment_api_v1"),
	path("comments/<int:comment_pk>/delete/", api_views.DeleteCommentAPIViewV1.as_view(), name="delete_comment_api_v1"),
]
