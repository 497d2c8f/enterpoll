from django.urls import path, include

from . import views, api_views

api_v1_patterns = [
	path("login/", api_views.LoginAPIViewV1.as_view(), name="login_api_v1"),
	path("logout/", api_views.LogoutAPIViewV1.as_view(), name="logout_api_v1"),
]

urlpatterns = [
    path("api/v1/", include(api_v1_patterns)),

	path("registration/", views.RegistrationView.as_view(), name="registration"),
	path("profile/<int:user_pk>/delete_user/", views.DeleteView.as_view(), name="delete_user"),
	path("login/", views.LoginView.as_view(), name="login"),
	path("logout/", views.logout, name="logout"),
	path("profile/<int:user_pk>/", views.ProfileView.as_view(), name="profile"),
	path("profile/<int:user_pk>/password_change", views.PasswordChangeView.as_view(), name="password_change"),
	path("profile/<int:user_pk>/password_change_done", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]
