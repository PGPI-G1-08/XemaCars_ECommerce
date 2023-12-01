FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ADD docker-settings.py /app/XemaCars_ECommerce/settings.py

ENV DJANGO_SETTINGS_MODULE=XemaCars_ECommerce.settings

CMD ["python", "manage.py", "collectstatic"]
