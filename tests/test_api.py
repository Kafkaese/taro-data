import requests
import os

API_HOST = os.environ['API_HOST']
API_PORT = os.environ['API_PORT']

# test for root endpoint 
def test_root_endpoint_status_code():
    URL = f'http://{API_HOST}:{API_PORT}/'
    
    response = requests.get(URL)

    assert response.status_code == 200

# tests for counry name endpoint
def test_metadata_name_short_endpoint_status_code():
    ENDPOINT = '/metadata/name/short'
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_metadata_name_short_request_status_code():
    ENDPOINT = '/metadata/name/short'
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA" 
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 501
    
# tests for "/metadata/democracy_index"
def test_metadata_democracy_index_endpoint_status_code():
    ENDPOINT = "/metadata/democracy_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_metadata_democracy_index_request_status_code():
    ENDPOINT = "/metadata/democracy_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_metadata_democracy_index_request():
    ENDPOINT = "/metadata/democracy_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 9.24

def test_metadata_democracy_index_request_missing():
    ENDPOINT = "/metadata/democracy_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 1778
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'

# test "/metadata/peace_index" endpoint
def test_metadata_peace_index_endpoint_status_code():
    ENDPOINT = "/metadata/peace_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_metadata_peace_index_request_status_code():
    ENDPOINT = "/metadata/peace_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_metadata_peace_index_request():
    ENDPOINT = "/metadata/peace_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 1.333
    
def test_metadata_peace_index_request_mssing():
    ENDPOINT = "/metadata/peace_index"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 1778
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
# test "/arms/exports/total" endpoint
def test_arms_exports_total_endpoint_status_code():
    ENDPOINT = "/arms/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_arms_exports_total_request_status_code():
    ENDPOINT = "/arms/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_arms_exports_total_request():
    ENDPOINT = "/arms/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 200_000_000
    
def test_arms_exports_total_request_mssing():
    ENDPOINT = "/arms/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 1778
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
# tests for "/arms/exports/timeseries" endpoint
def test_arms_exports_timeseries_endpoint_status_code():
    ENDPOINT = "/arms/exports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_arms_exports_total_timeseries_status_code():
    ENDPOINT = "/arms/exports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_arms_exports_timeseries_request():
    ENDPOINT = "/arms/exports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA"
    }
    
    response = requests.get(URL, params=PARAMS).json()
    
    assert type(response) == list
    assert list(response[0].keys()) == ['year', 'value']
    
def test_arms_exports_timeseries_request_mssing():
    ENDPOINT = "/arms/exports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "XX"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'