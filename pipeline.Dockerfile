FROM python:3.8-bookworm

# Upgrade pip
RUN pip install pip --upgrade

# Install taro package
COPY setup.py setup.py
COPY taro/ taro
COPY requirements.txt requirements.txt
RUN pip install .

# Copy csv data
COPY data/ data
COPY raw_data/ raw_data

# Run pipelines
CMD ["python", "/taro/pipeline.py"]
