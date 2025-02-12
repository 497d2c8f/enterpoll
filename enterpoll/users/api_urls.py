from django.urls import path
from . import api_views


urlpatterns = [
	path("registration/", api_views.RegistrationAPIViewV1.as_view(), name="registration_api_v1"),
	path("login/", api_views.LoginAPIViewV1.as_view(), name="login_api_v1"),
	path("logout/", api_views.LogoutAPIViewV1.as_view(), name="logout_api_v1"),
	path("<int:user_pk>/profile/", api_views.ProfileAPIViewV1.as_view(), name="profile_api_v1"),
	path("<int:user_pk>/profile/poll_list/", api_views.UserPollListAPIViewV1.as_view(), name="user_poll_list_api_v1"),
	path("<int:user_pk>/profile/vote_list/", api_views.UserVoteListAPIViewV1.as_view(), name="user_vote_list_api_v1"),
	path("<int:user_pk>/profile/rating_list/", api_views.UserRatingListAPIViewV1.as_view(), name="user_rating_list_api_v1"),
	path("<int:user_pk>/profile/comment_list/", api_views.UserCommentListAPIViewV1.as_view(), name="user_comment_list_api_v1"),
	path("<int:user_pk>/profile/password_change/", api_views.PasswordChangeAPIViewV1.as_view(), name="password_change_api_v1"),
	path("<int:user_pk>/profile/delete/", api_views.DeleteAPIViewV1.as_view(), name="delete_user_api_v1"),
]
