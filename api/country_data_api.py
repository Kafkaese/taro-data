from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from sqlalchemy import create_engine, sql
import os
import pandas as pd

## APP
app = Flask(__name__)


## CORS settings

CORS(app)


## database connection

host = os.environ['POSTGRES_HOST']
dbname = os.environ['POSTGRES_DB']

# Use tf vars if not local dev env
if os.environ['ENV'] == 'dev' or os.environ['ENV'] == 'test':
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
else:    
    user = os.environ['TF_VAR_postgres_user']
    password = os.environ['TF_VAR_postgres_password']

sslmode = "require"
    
# Construct connection string
print(f"USING ENV: {os.environ['ENV']}")
conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{5432}/{dbname}"

# Cet up connecttion
print(f"Connecting to: {conn_string}")
db = create_engine(conn_string)
conn = db.connect()


# root endpoint
@app.route("/", methods=["GET"])
async def root():
    
    return jsonify({'status': 200})


# metadata path endpoints

@app.route("/metadata/name/short", methods=["GET"])
async def short_name():
    
    country_code = request.args.get("country_code")
    
    global conn
        
    query = sql.text('''select short_name from country_names where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        
        result = cursor.fetchall()
    
        if result == []:
            return jsonify({'value': 'no data'})
        
        return jsonify({'value': result[0][0]} )
    
    # if year < 2008 throws error because columns does not exist
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})
    
@app.route("/metadata/democracy_index", methods=["GET"])
async def democracy_index():

    country_code = request.args.get("country_code")
    year = request.args.get("year")

    global conn
    
    # columns cannot be passed as parameters
    query = sql.text(f'''select "{year}" from democracy_index where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        
        result = cursor.fetchall()
    
        if result == []:
            return jsonify({'value': 'no data'})
        
        return jsonify({'value': result[0][0]}) 
    
    # if year < 2008 throws error because columns does not exist
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})
    
@app.route("/metadata/peace_index", methods=["GET"])
async def peace_index():

    country_code = request.args.get("country_code")
    year = request.args.get("year")
    
    global conn

    # columns cannot be passed as parameters
    query = sql.text(f'''select "{year}" from peace_index where "Alpha-2 code" = :c;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code})
        
        result = cursor.fetchall()
    
        if result == []:
            return jsonify({'value': 'no data'})
        
        return jsonify({'value': result[0][0]} )
    
    # if year < 2008 throws error because columns does not exist
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})
    
    

# arms path endpoints

# arms/export

@app.route("/arms/exports/total", methods=["GET"])
async def arms_exports_total():
   
    country_code = request.args.get("country_code")
    year = request.args.get("year")
    
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
                return jsonify({'value': 'no data'})
        
        return jsonify({'value': result[0][0]} )   
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})



@app.route("/arms/exports/timeseries", methods=["GET"])
async def arms_exports_timeseries():
    
    country_code = request.args.get("country_code")
    
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
            return jsonify({'value': 'no data'})
      
        return jsonify([{'year': year[0], 'value': int(year[1])} for year in result])
    
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})

# Gets export data for a country on a given year, listing values for source counries seperately
@app.route("/arms/exports/by_country", methods=["GET"])
async def arms_exports_by_country():
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
    
    country_code = request.args.get("country_code")
    year = request.args.get("year")
    limit = request.args.get("year", default=300)
    
    global conn
    
    query = sql.text('''select "Destination country", "Value", "short_name" from arms
        join country_names on "Destination country"="Alpha-2 code"
        where "Source country" = :c and "Year" = :y
        order by "Value" desc limit :l;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year, 'l': limit})
        result = cursor.fetchall()
        
        if result == []:
            return jsonify({'value': 'no data'})
        
        return jsonify([{'name': country[0], 'value': country[1], 'full_name': country[2]} for country in result])
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})
    
# arms/import path endpoints

@app.route("/arms/imports/total", methods=["GET"])
async def arms_imports_total():
        
    country_code = request.args.get("country_code")
    year = request.args.get("year")
    
    global conn
    
    query = sql.text('''select SUM("Value") from arms where "Destination country" = :c and "Year" = :y;''')
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
        result = cursor.fetchall()
        
         # If aggregate function is used, result will not be empty, but NULL
        if result[0] == (None,):
            
            return jsonify({'value': 'no data'})
        
        return {'value': result[0][0]}
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})
    

@app.route("/arms/imports/by_country", methods=["GET"])
async def arms_imports_by_country():
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
    
    country_code = request.args.get("country_code")
    year = request.args.get("year")
    limit = request.args.get("year", default=300)
    
    global conn
    
    query = sql.text('''select "Source country", "Value", "short_name" from arms
        join country_names on "Source country"="Alpha-2 code"
        where "Destination country" = :c and "Year" = :y
        order by "Value" desc limit :l;''')
    
    try:
        cursor = conn.execute(query, parameters = {'c': country_code, 'y': year, 'l': limit})
        result = cursor.fetchall()
        
        if result == []:
            return jsonify({'value': 'no data'})
        
        return jsonify([{'name': country[0], 'value': country[1], 'full_name': country[2]} for country in result])
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})
    
# Gets time series of total import values per year for a given country
@app.route("/arms/imports/timeseries", methods=["GET"])
async def arms_imports_timeseries():
    
        
    country_code = request.args.get("country_code")
    
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
            return jsonify({'value': 'no data'})
      
        return jsonify([{'year': year[0], 'value': int(year[1])} for year in result])
    
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})
    
    
# merchandise path endpoints

@app.route("/merchandise/exports/total", methods=["GET"])
async def exports_merchandise_year():
    
        
    country_code = request.args.get("country_code")
    year = request.args.get("year")

    global conn
    
    query = sql.text('''select SUM(export_value) from merchandise_exports
        join country_names as cn on "country_id" = cn."index"
        where "Alpha-2 code" = :c and year = :y;''')
    
    cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
    
    try:
        result = cursor.fetchall()
  
        if result[0] == (None,):
            return jsonify({'value': 'no data'})
        
        return jsonify({'value': result[0][0]} )   
    except:
        conn.close()
        conn = db.connect()
        return jsonify({'value': 'no data'})

# Dev only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)