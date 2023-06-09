from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from sqlalchemy import create_engine, sql

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

# database connection
conn_string = 'postgresql://postgres:password@taro-postgres/postgres'
db = create_engine(conn_string)
conn = db.connect()



# metadata
metadata = pd.read_csv('data/metadata.csv',  index_col=0)
democracy_index_data = pd.read_csv('data/democracy_index.csv',  index_col=0)
peace_index_data = pd.read_csv('data/peace_index.csv', index_col=0)

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
    
@app.get("/metadata/peace_index")
async def peace_index(country_code, year):
    #print(country_name)
    #print(democracy_index_data.loc[country_name, year])
    
    try:
        return {'value': str(peace_index_data.loc[country_code, year])}
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

@app.get("/exports/year")
async def exports_year(country_code, year):
    print(country_code)
    print(year)
    query = sql.text('''select * from exports where "Source country" = :c and "Year" = :y;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
    result = cursor.fetchall()
    print(result)
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}    

# import path endpoints

@app.get("/imports/year")
async def imports_year(country_code, year):
    
    query = sql.text('''select * from imports where "Destination country" = :c and "Year" = :y;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
    result = cursor.fetchall()
    
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}
    