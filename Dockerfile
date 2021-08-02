FROM python:3.9.0

WORKDIR /home/

RUN echo "test ku sandbox"

RUN git clone https://github.com/matt700395/kusandbox.git

WORKDIR /home/kusandbox/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt requriements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=kusandbox.settings.deploy && python manage.py migrate --settings=kusandbox.settings.deploy && gunicorn kusandbox.wsgi --env DJANGO_SETTINGS_MODULE=kusandbox.settings.deploy --bind 0.0.0.0:8000"]
