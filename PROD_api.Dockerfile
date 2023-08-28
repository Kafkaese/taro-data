FROM python:latest

COPY PROD_requirements_api.txt requirements.txt

RUN pip install -r requirements.txt

COPY api/ api

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api.country_data_api:app"]