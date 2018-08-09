sleep 10
python manage.py makemigrations flush
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'qwerty123')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin1', 'admin1@example.com', 'qwerty123')" | python manage.py shell
python manage.py makemigrations exchange
python manage.py migrate
python manage.py test
python manage.py runserver 0.0.0.0:8000
