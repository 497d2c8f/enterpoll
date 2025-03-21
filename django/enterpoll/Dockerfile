from python:3
workdir /django/enterpoll/
copy requirements .
run pip install --upgrade pip && pip install -r requirements
copy . .
entrypoint \
	python3 mysite/manage.py collectstatic --noinput && \
	python3 mysite/manage.py makemigrations && \
	python3 mysite/manage.py migrate && \
#	pytest && \
#	python3 mysite/manage.py shell --command='import fill_the_site_with_data' && \
	cd mysite && \
	/usr/local/bin/gunicorn \
		--access-logfile '-' \
		--bind django-enterpoll:80 \
		mysite.wsgi:application
