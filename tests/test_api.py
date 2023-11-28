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
    
    assert response.status_code == 200
    
def test_metadata_name_short_request():
    ENDPOINT = '/metadata/name/short'
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA" 
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == "Canada"
    
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
    
def test_metadata_peace_index_request_missing():
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
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_arms_exports_total_request():
    ENDPOINT = "/arms/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 200_000_000
    
def test_arms_exports_total_request_missing():
    ENDPOINT = "/arms/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 1778,
        "currency": "EUR"
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
    
def test_arms_exports_timeseries_request_missing():
    ENDPOINT = "/arms/exports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "XX"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
# tests for "/arms/exports/by_country" endpoint
def test_arms_exports_by_ountry_endpoint_status_code():
    ENDPOINT = "/arms/exports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_arms_exports_by_country_status_code():
    ENDPOINT = "/arms/exports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA",
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_arms_exports_by_country_request():
    ENDPOINT = "/arms/exports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "FR",
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS).json()
    
    assert type(response) == list
    assert list(response[0].keys()) == ['name', 'value', 'full_name']
    
def test_arms_exports_by_country_request_missing():
    ENDPOINT = "/arms/exports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "XX",
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
# test for "/arms/imports/total" endpoint
def test_arms_imports_total_endpoint_status_code():
    ENDPOINT = "/arms/imports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_arms_imports_total_request_status_code():
    ENDPOINT = "/arms/imports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_arms_imports_total_request():
    ENDPOINT = "/arms/imports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 112_625_579
    
def test_arms_imports_total_request_missing():
    ENDPOINT = "/arms/imports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 1778,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
# tests for "/arms/imports/timeseries" endpoint
def test_arms_exports_timeseries_endpoint_status_code():
    ENDPOINT = "/arms/imports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_arms_imports_total_timeseries_status_code():
    ENDPOINT = "/arms/imports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA",
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_arms_imports_timeseries_request():
    ENDPOINT = "/arms/imports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA",
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS).json()
    
    assert type(response) == list
    assert list(response[0].keys()) == ['year', 'value']
    
def test_arms_imports_timeseries_request_missing():
    ENDPOINT = "/arms/imports/timeseries"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "XX",
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
# tests for "/arms/exports/by_country" endpoint
def test_arms_imports_by_ountry_endpoint_status_code():
    ENDPOINT = "/arms/imports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_arms_imports_by_country_status_code():
    ENDPOINT = "/arms/imports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA",
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_arms_imports_by_country_request():
    ENDPOINT = "/arms/imports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA",
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS).json()
    
    assert type(response) == list
    assert list(response[0].keys()) == ['name', 'value', 'full_name']
    
def test_arms_imports_by_country_request_missing():
    ENDPOINT = "/arms/imports/by_country"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "XX",
        "year": 2020,
        "currency": "EUR"
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
# tests for "/merchandise/exports/total" endpoint
def test_merchandise_exports_total_endpoint_status_code():
    ENDPOINT = "/merchandise/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    response = requests.get(URL)
    
    assert response.status_code == 422
    
def test_merchandise_exports_total_request_status_code():
    ENDPOINT = "/merchandise/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.status_code == 200

def test_merchandise_exports_total_request():
    ENDPOINT = "/merchandise/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 2020
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 390_762.62845
    
def test_merchandise_exports_total_request_missing():
    ENDPOINT = "/merchandise/exports/total"
    URL = f'http://{API_HOST}:{API_PORT}{ENDPOINT}'
    
    PARAMS = {
        "country_code": "CA", 
        "year": 1778
    }
    
    response = requests.get(URL, params=PARAMS)
    
    assert response.json()['value'] == 'no data'
    
