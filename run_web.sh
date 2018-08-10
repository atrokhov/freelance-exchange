sleep 10
python manage.py makemigrations exchange
python manage.py migrate
python manage.py test
python manage.py runserver 0.0.0.0:8000
