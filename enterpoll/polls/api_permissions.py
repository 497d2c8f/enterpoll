from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsAuthorOrAdmin(permissions.BasePermission):

	message = _('The action is available only to the author or the admin.')
	code = 'forbidden'

	def has_object_permission(self, request, view, obj):
#		if request.method in permissions.SAFE_METHODS:
#			return True
		return obj.user == request.user or request.user.is_staff
