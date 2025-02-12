from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsAuthorOrAdmin(permissions.BasePermission):

	code = 'forbidden'

	def has_object_permission(self, request, view, obj):
#		if request.method in permissions.SAFE_METHODS:
#			return True
		self.message = _(f'The action is available only to the user ({obj.user.username}) or the admin.')
		return obj.user == request.user or request.user.is_staff
