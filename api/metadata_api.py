from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata = pd.read_csv('data/metadata.csv',  index_col=0)

@app.get("/")
async def root():
    return {'status': 200}

@app.get("/info/name")
async def name(country_code):
    print(country_code)
    print(metadata.loc[country_code, 'name'])
    
    try:
        return {'value': str(metadata.loc[country_code, 'name'])}
    except:
        return {'value': 'no data'}
    
