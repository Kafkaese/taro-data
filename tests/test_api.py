import requests
import os

API_HOST = os.environ['API_HOST']
API_PORT = os.environ['API_PORT']

def test_root_endpoint_status_code():
    URL = f'http://{API_HOST}:{API_PORT}/'
    
    response = requests.get(URL)
    print(response.status_code)
    assert response.status_code == 200