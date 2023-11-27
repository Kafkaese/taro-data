FROM python:latest

COPY requirements_api.txt requirements.txt

RUN pip install -r requirements.txt

COPY api/ api

# ENVs needed to be provided on run-time:
# POSTGRES_HOST
# POSTGRES_PORT
# POSTGRES_USER
# POSTGRES_PASSWORD

CMD ["uvicorn", "--host", "0.0.0.0", "api.country_data_api:app", "--ssl-keyfile=./example.com+5-key.pem", "--ssl-certfile=./example.com+5.pem"]