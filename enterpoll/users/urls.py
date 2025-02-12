from django.urls import path
from . import views


urlpatterns = [
	path("registration/", views.RegistrationView.as_view(), name="registration"),
	path("<int:user_pk>/profile/delete_user/", views.DeleteView.as_view(), name="delete_user"),
	path("login/", views.LoginView.as_view(), name="login"),
	path("logout/", views.logout, name="logout"),
	path("<int:user_pk>/profile/", views.ProfileView.as_view(), name="profile"),
	path("<int:user_pk>/profile/password_change", views.PasswordChangeView.as_view(), name="password_change"),
	path("<int:user_pk>/profile/password_change_done", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]
