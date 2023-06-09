FROM python:latest

COPY api/ api

# remove once data comes from psql
COPY data/ data

COPY requirements_api.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "api.country_data_api:app"]