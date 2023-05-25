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

total_imports_data = pd.read_csv('data/total_imports.csv',  index_col=0)

democracy_index_data = pd.read_csv('data/democracy_index.csv',  index_col=0)

@app.get("/")
async def root():
    return {'status': 200}

@app.get("/total_imports")
async def total(country_name):
    #print(country_name)
    #print(data.loc[country_name, 'Value'])
    
    try:
        return {'value': str(total_imports_data.loc[country_name, 'Value'])}
    except:
        return {'value': 'no data'}
    
@app.get("/democracy_index")
async def total(country_name, year):
    #print(country_name)
    #print(democracy_index_data.loc[country_name, year])
    
    try:
        return {'value': str(democracy_index_data.loc[country_name, year])}
    except:
        return {'value': 'no data'}
