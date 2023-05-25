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

# metadata
metadata = pd.read_csv('data/metadata.csv',  index_col=0)
democracy_index_data = pd.read_csv('data/democracy_index.csv',  index_col=0)

# exports data
export_total_data = pd.read_csv('data/total_exports.csv',  index_col=0)

# import data
total_imports_data = pd.read_csv('data/total_imports.csv',  index_col=0)



# root endpoint

@app.get("/")
async def root():
    return {'status': 200}


# metadata path endpoints

@app.get("/metadata/name")
async def name(country_code):
    print(country_code)
    print(metadata.loc[country_code, 'name'])
    
    try:
        return {'value': str(metadata.loc[country_code, 'name'])}
    except:
        return {'value': 'no data'}
    
@app.get("/metadata/democracy_index")
async def democracy_index(country_code, year):
    #print(country_name)
    #print(democracy_index_data.loc[country_name, year])
    
    try:
        return {'value': str(democracy_index_data.loc[country_code, year])}
    except:
        return {'value': 'no data'}


# exports path endpoints

@app.get("/exports/total")
async def exports_total(country_code):
    #print(country_name)
    #print(data.loc[country_name, 'Value'])
    
    try:
        return {'value': str(export_total_data.loc[country_code, 'Value'])}
    except:
        return {'value': 'no data'}


# import path endpoints

@app.get("/imports/total")
async def imports_total(country_code):
    #print(country_name)
    #print(data.loc[country_name, 'Value'])
    
    try:
        return {'value': str(total_imports_data.loc[country_code, 'Value'])}
    except:
        return {'value': 'no data'}
    