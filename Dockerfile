FROM python:3.13
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
# Install dependencies via pyproject.toml
COPY pyproject.toml /code/

# Copy application code
COPY WBSAtool /code/WBSAtool
COPY WBSAtool/manage.py /code/manage.py

# Install the project
RUN pip install .

# Static files volume
RUN mkdir /static
VOLUME /static

# Copy startup script that will run scripts
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8000

# Entrypoint runs scripts then executes the container CMD
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["gunicorn", "WBSAtool.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]