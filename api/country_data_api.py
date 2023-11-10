from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from sqlalchemy import create_engine, sql
import os
import pandas as pd

app = FastAPI()

## CORS settings

env = os.environ['ENV']
frontend_host = os.environ['REACT_HOST']

if env == 'production':
    origins = [f"http://{frontend_host}",
               "https://www.arms-tracker.app"]

else:
        origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


## database connection

host = os.environ['POSTGRES_HOST']
dbname = os.environ['POSTGRES_DB']
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']


sslmode = "require"
    
# Construct connection string
print(f"USING ENV: {os.environ['ENV']}")
conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{5432}/{dbname}"

# Cet up connecttion
print(f"Connecting to: {conn_string}")
db = create_engine(conn_string)
conn = db.connect()


# root endpoint

@app.get("/")
async def root():
    
    return {'status': 200}


# metadata path endpoints

@app.get("/metadata/name/short")
async def short_name(country_code):
    
    global conn
        
    query = sql.text('''select short_name from country_names where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        
        result = cursor.fetchall()
    
        if result == []:
            return {'value': 'no data'}
        
        return {'value': result[0][0]} 
    
    # if year < 2008 throws error because columns does not exist
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
    
@app.get("/metadata/democracy_index")
async def democracy_index(country_code, year):

    global conn
    
    # columns cannot be passed as parameters
    query = sql.text(f'''select "{year}" from democracy_index where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        
        result = cursor.fetchall()
    
        if result == []:
            return {'value': 'no data'}
        
        return {'value': result[0][0]} 
    
    # if year < 2008 throws error because columns does not exist
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
    
@app.get("/metadata/peace_index")
async def peace_index(country_code, year):

    global conn

    # columns cannot be passed as parameters
    query = sql.text(f'''select "{year}" from peace_index where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        
        result = cursor.fetchall()
    
        if result == []:
            return {'value': 'no data'}
        
        return {'value': result[0][0]} 
    
    # if year < 2008 throws error because columns does not exist
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
    
    

# arms path endpoints

# arms/export

@app.get("/arms/exports/total")
async def arms_exports_total(country_code, year):
   
    global conn
   
    print('HERE')
    query = sql.text('''select SUM("Value") from arms where "Source country" = :c and "Year" = :y;''')
    backup_query = sql.text('''select "Value" from exports where "Source country" = :c and "Year" = :y;''')

    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
        
        result = cursor.fetchall()
        
        # If aggregate function is used, result will not be empty, but NULL
        if result[0] == (None,):
            
            # Query exports table if no data was found on arms table
            cursor = conn.execute(backup_query, parameters = {'c': country_code, 'y': year})
            result = cursor.fetchall()
            
            # Still nothing? -> no data
            if result == []:
                return {'value': 'no data'}
        
        return {'value': result[0][0]}    
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}



@app.get("/arms/exports/timeseries")
async def arms_exports_timeseries(country_code):
    global conn
    
    query = sql.text('''select coalesce (arms."Year", exports."Year"), coalesce (arms.sum, exports.sum) from 
        (
        select "Year", SUM("Value") from arms
                        where "Source country" = :c
                        group by "Year"
                        order by "Year" asc
        ) as arms
        full outer join
        (
        select "Year", SUM("Value") from exports
        where "Source country" = :c
        group by "Year"
        order by "Year" asc 
        ) as exports
        on arms."Year" = exports."Year" ;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        result = cursor.fetchall()
        
        if result == []:
            return {'value': 'no data'}
      
        return [{'year': year[0], 'value': int(year[1])} for year in result]
    
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}

# Gets export data for a country on a given year, listing values for source counries seperately
@app.get("/arms/exports/by_country")
async def arms_exports_by_country(country_code, year, limit=300):
    '''
    Gets export data for a country on a given year, listing values for source countries seperately.
    
    Paramaters:
        country_code (string): Alpha-2 country code
        year (string): Year of the data
    
        limit (int): Number of source countries to return. Returns top n by export value for the given year.

    Returns:
        Dictionary or List of Dictionaries: 
             Individual country information in dictionary with: {name, value, full_name}
             Single dictionary with {'value': 'no data'} in case of missing data.
    '''
    
    global conn
    
    query = sql.text('''select "Destination country", "Value", "short_name" from arms
        join country_names on "Destination country"="Alpha-2 code"
        where "Source country" = :c and "Year" = :y
        order by "Value" desc limit :l;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year, 'l': limit})
        result = cursor.fetchall()
        
        if result == []:
            return {'value': 'no data'}
        
        return [{'name': country[0], 'value': country[1], 'full_name': country[2]} for country in result]
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
    
# arms/import path endpoints

@app.get("/arms/imports/total")
async def arms_imports_total(country_code, year):
    
    global conn
    
    query = sql.text('''select SUM("Value") from arms where "Destination country" = :c and "Year" = :y;''')
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
        result = cursor.fetchall()
        
         # If aggregate function is used, result will not be empty, but NULL
        if result[0] == (None,):
            
            return {'value': 'no data'}
        
        return {'value': result[0][0]}
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
    

@app.get("/arms/imports/by_country")
async def arms_imports_by_country(country_code, year, limit=300):
    '''
    Gets import data for a country on a given year, listing values for source countries seperately.
    
    Paramaters:
        country_code (string): Alpha-2 country code
        year (string): Year of the data
    
        limit (int): Number of source countries to return. Returns top n by import value for the given year.

    Returns:
        Dictionary or List of Dictionaries: 
             Individual country information in dictionary with: {name, value, full_name}
             Single dictionary with {'value': 'no data'} in case of missing data.
    '''
    
    global conn
    
    query = sql.text('''select "Source country", "Value", "short_name" from arms
        join country_names on "Source country"="Alpha-2 code"
        where "Destination country" = :c and "Year" = :y
        order by "Value" desc limit :l;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year, 'l': limit})
        result = cursor.fetchall()
        
        if result == []:
            return {'value': 'no data'}
        
        return [{'name': country[0], 'value': country[1], 'full_name': country[2]} for country in result]
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
    
# Gets time series of total import values per year for a given country
@app.get("/arms/imports/timeseries")
async def arms_imports_timeseries(country_code):
    global conn
    
    query = sql.text('''select coalesce (arms."Year", imports."Year"), coalesce (arms.sum, imports.sum) from 
        (
        select "Year", SUM("Value") from arms
                        where "Destination country" = :c
                        group by "Year"
                        order by "Year" asc
        ) as arms
        full outer join
        (
        select "Year", SUM("Value") from imports
        where "Destination country" = :c
        group by "Year"
        order by "Year" asc 
        ) as imports
        on arms."Year" = imports."Year" ;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        result = cursor.fetchall()
        
        if result == []:
            return {'value': 'no data'}
      
        return [{'year': year[0], 'value': int(year[1])} for year in result]
    
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
    
    
# merchandise path endpoints

@app.get("/merchandise/exports/total")
async def exports_merchandise_year(country_code, year):

    global conn
    
    query = sql.text('''select SUM(export_value) from merchandise_exports
        join country_names as cn on "country_id" = cn."index"
        where "Alpha-2 code" = :c and year = :y;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
    
    try:
        result = cursor.fetchall()
  
        if result[0] == (None,):
            return {'value': 'no data'}
        
        return {'value': result[0][0]}    
    except:
        conn.close()
        conn = db.connect()
        return {'value': 'no data'}
