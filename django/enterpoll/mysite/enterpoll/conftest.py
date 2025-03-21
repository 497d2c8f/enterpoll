import pytest


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
	from django.conf import settings
	settings.DATABASES['default'] = {
		'ENGINE': 'django.db.backends.postgresql',
		'HOST': 'postgresql',
		'PORT': 5432,
		'NAME': 'postgres',
		'USER': 'postgres',
		'ATOMIC_REQUESTS': False,
	}

	with django_db_blocker.unblock():
		import fill_the_site_with_data_for_test
