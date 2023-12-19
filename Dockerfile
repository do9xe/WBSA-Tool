FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY WBSAtool /code/

RUN mkdir /static
VOLUME /static
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

EXPOSE 8000
CMD gunicorn WBSAtool.wsgi:application --bind 0.0.0.0:8000 --workers 2