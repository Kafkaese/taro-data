from fastapi import FastAPI
import pandas as pd

api = FastAPI()

data = pd.read_csv('data/total_exports.csv')

@api.get("/")
async def root():
    return {'status': 200}

@api.get("/total{country_name}")
async def total(country_name):
    try:
        return {'value': data[country_name, 'Value']}
    except:
        return {'value': 'no data'}
