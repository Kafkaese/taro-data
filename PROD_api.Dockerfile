FROM python:latest

COPY PROD_requirements_api.txt requirements.txt

RUN pip install -r requirements.txt

COPY api/ api

RUN touch access.log error.log

COPY gunicorn_config.py gunicorn_config.py

CMD ["gunicorn", "-c", "gunicorn_config.py", "api.country_data_api:app"]