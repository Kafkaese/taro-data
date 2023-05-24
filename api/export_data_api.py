from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

api = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data = pd.read_csv('data/total_exports.csv',  index_col=0)

@api.get("/")
async def root():
    return {'status': 200}

@api.get("/total")
async def total(country_name):
    #print(country_name)
    #print(data.loc[country_name, 'Value'])
    
    try:
        return {'value': str(data.loc[country_name, 'Value'])}
    except:
        return {'value': 'no data'}
