FROM python:latest

# Upgrade pip
RUN pip install pip --upgrade

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy csv data
COPY data/ data

# Copy pipeline
COPY taro/ taro

# Set workdir to taro
WORKDIR /taro

# Run pipelines
CMD ["python", "pipeline.py"]
