web: gunicorn NanoPayApi.wsgi
release : python mannage.py makemigrations --noinput
release : python mannage.py collectstatic --noinput
release : python mannage.py migrate --noinput