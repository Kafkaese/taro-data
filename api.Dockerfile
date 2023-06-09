FROM python:latest

COPY requirements_api.txt requirements.txt

RUN pip install -r requirements.txt

COPY api/ api

CMD ["uvicorn", "--host", "0.0.0.0", "api.country_data_api:app"]