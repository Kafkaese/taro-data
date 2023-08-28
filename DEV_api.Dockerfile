FROM python:latest

COPY DEV_requirements_api.txt requirements.txt

RUN pip install -r requirements.txt

COPY api/ api

CMD ["python", "api/country_data_api.py"]