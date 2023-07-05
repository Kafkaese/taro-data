FROM python:latest

# Upgrade pip
RUN pip install pip --upgrade

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy csv data
COPY data/ data

# Copy pipeline
COPY taro/pipeline.py pipeline.py

CMD ["python", "pipeline.py"]
