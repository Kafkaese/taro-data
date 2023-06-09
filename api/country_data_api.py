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


# root endpoint

@app.get("/")
async def root():
    
    return {'status': 200}


# metadata path endpoints

@app.get("/metadata/name")
async def name(country_code):
    query = sql.text('''select short_name from country_names where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        
        result = cursor.fetchall()
    
        if result == []:
            return {'value': 'no data'}
        
        return {'value': result[0][0]} 
    
    # if year < 2008 throws error because columns does not exist
    except:
        return {'value': 'no data'}
    
@app.get("/metadata/democracy_index")
async def democracy_index(country_code, year):

    query = sql.text('''select :y from peace_index where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
        
        result = cursor.fetchall()
    
        if result == []:
            return {'value': 'no data'}
        
        return {'value': result[0][0]} 
    
    # if year < 2008 throws error because columns does not exist
    except:
        return {'value': 'no data'}
    
@app.get("/metadata/peace_index")
async def peace_index(country_code, year):

    query = sql.text('''select :y from peace_index where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
        
        result = cursor.fetchall()
    
        if result == []:
            return {'value': 'no data'}
        
        return {'value': result[0][0]} 
    
    # if year < 2008 throws error because columns does not exist
    except:
        return {'value': 'no data'}
    
    

# exports path endpoints

@app.get("/exports/arms/total")
async def exports_arms_total(country_code):

    query = sql.text('''select SUM("Value") from exports where "Source country" = :c;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code})
    
    result = cursor.fetchall()
    
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}  

@app.get("/exports/arms/year")
async def exports_arms_year(country_code, year):
   
    query = sql.text('''select "Value" from exports where "Source country" = :c and "Year" = :y;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
    
    result = cursor.fetchall()
    
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}    

@app.get("/exports/merchandise/total")
async def exports_merchandise_total(country_code):

    query = sql.text('''select SUM("export_alue") from merchandise_exports where "country_id" = :c;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code})
    
    result = cursor.fetchall()
    
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}  

@app.get("/exports/merchandise/year")
async def exports_merchandise_year(country_code, year):
   
    query = sql.text('''select "export_value" from exports where "country_id" = :c and "year" = :y;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
    
    result = cursor.fetchall()
    
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}    


# import path endpoints

@app.get("/imports/arms/total")
async def imports_arms_total(country_code):

    query = sql.text('''select SUM("Value") from imports where "Destination country" = :c;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code})
    
    result = cursor.fetchall()
    
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}  

@app.get("/imports/year")
async def imports_arms_year(country_code, year):
    
    query = sql.text('''select "Value" from imports where "Destination country" = :c and "Year" = :y;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
    result = cursor.fetchall()
    
    if result == []:
        return {'value': 'no data'}
    
    return {'value': result[0][0]}
    