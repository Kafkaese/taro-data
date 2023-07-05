FROM python:latest

# Upgrade pip
RUN pip install pip --upgrade

# Install taro package
COPY setup.py setup.py
COPY taro/ taro
COPY requirements.txt requirements.txt
RUN pip install .

# Copy csv data
COPY data/ data

# Run pipelines
CMD ["python", "/taro/pipeline.py"]
