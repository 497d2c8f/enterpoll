"""
URL configuration for enterpoll project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from django.shortcuts import render

urlpatterns = [
	path('admin/', admin.site.urls),
	path('users/', include('users.urls')),
	path('enterpoll/', include('polls.urls')),
	path(
		'api/',
		include([
			path('users/', include('users.api_urls')),
			path('enterpoll/', include('polls.api_urls'))
		])
	),
]

handler404 = lambda request, exception: render(request, template_name='404.html', status=404)

admin.site.site_header = 'EnterPoll'
admin.site.index_title = 'EnterPoll'
admin.site.site_title = 'Admin'
admin.site.site_url = reverse('main_page')
