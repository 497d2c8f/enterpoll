from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):

	has_add_permission = lambda *args: False
	readonly_fields = [
		'username',
		'password',
		'first_name',
		'last_name',
		'email',
		'is_active',
		'last_login',
		'date_joined'
	]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

#from pprint import pprint as pp
#pp(CustomUserAdmin.search_fields)

#admin.site.unregister(Group)
