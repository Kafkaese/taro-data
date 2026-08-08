from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, sql
from mangum import Mangum
import os
import re

app = FastAPI()

## CORS settings

env = os.environ['ENV']

if env == 'production':
    # dev.arms-tracker.app deliberately shares this same backend rather than
    # getting its own - the API is entirely read-only (allow_methods=["GET"]
    # below), so there's no write-isolation reason to stand up a separate
    # one just for a dev frontend to hit.
    origins = ["https://www.arms-tracker.app",
               "https://arms-tracker.app",
               "https://dev.arms-tracker.app"]

else:
        origins = [
        "https://localhost",
        "https://localhost:3000",
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
port = os.environ.get('POSTGRES_PORT', 5432)
dbname = os.environ['POSTGRES_DB']
user = os.environ['POSTGRES_USER']

# In Lambda, the password isn't passed directly as an env var - only the
# name of the SSM parameter holding it is, and this fetches+decrypts it at
# module load time (once per execution environment, not per-request, since
# Lambda reuses warm environments across invocations). Falls back to a
# plain POSTGRES_PASSWORD for local/docker-compose dev, which has no SSM
# access and no reason to need it.
password_param = os.environ.get('POSTGRES_PASSWORD_PARAM')
if password_param:
    import boto3
    ssm = boto3.client('ssm')
    password = ssm.get_parameter(Name=password_param, WithDecryption=True)['Parameter']['Value']
else:
    password = os.environ['POSTGRES_PASSWORD']


sslmode = "require"

# Construct connection string
print(f"USING ENV: {os.environ['ENV']}")
conn_string = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"

# pool_pre_ping validates a pooled connection before handing it out and
# transparently reconnects if it's gone stale. Matters specifically for
# Lambda: an execution environment can sit frozen between invocations for
# long enough that Postgres (or something in between) has already closed
# the connection by the time it thaws, and without this the first request
# after a freeze would silently fail. Connections are also now acquired
# per-request (see each endpoint) instead of one held for the process's
# entire lifetime, which used to mean every concurrent request shared a
# single connection object.
print(f"Connecting to: {conn_string}")
db = create_engine(conn_string, pool_pre_ping=True)

# valid currencies
VALID_CURRENCIES = ['EUR', 'USD']

# `year` is spliced directly into a few queries below as a column
# identifier (SQLAlchemy can't bind identifiers as parameters), so it needs
# its own allow-list check the same way `currency` gets one - a bare regex
# match rather than e.g. int(year) so it also rejects things like leading
# '+'/whitespace that int() would silently accept.
YEAR_RE = re.compile(r'^\d{4}$')

# root endpoint

@app.get("/")
async def root():

    return {'status': 200}

# metadata path endpoints

@app.get("/metadata/name/short")
async def short_name(country_code):

    query = sql.text('''select short_name from country_names where "Alpha-2 code" = :c;''')

    try:
        with db.connect() as conn:
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

    if not YEAR_RE.match(year):
        return {'value': 'no data'}

    # columns cannot be passed as parameters
    query = sql.text(f'''select "{year}" from democracy_index where "Alpha-2 code" = :c;''')

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'c': country_code})
            result = cursor.fetchall()

        if result == []:
            return {'value': 'no data'}

        return {'value': result[0][0]}

    # if year < 2008 throws error because columns does not exist
    except:
        return {'value': 'no data'}

@app.get("/metadata/peace_index")
async def peace_index(country_code, year):

    if not YEAR_RE.match(year):
        return {'value': 'no data'}

    # columns cannot be passed as parameters
    query = sql.text(f'''select "{year}" from peace_index where "Alpha-2 code" = :c;''')

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'c': country_code})
            result = cursor.fetchall()

        if result == []:
            return {'value': 'no data'}

        return {'value': result[0][0]}

    # if year < 2008 throws error because columns does not exist
    except:
        return {'value': 'no data'}



# arms path endpoints

# arms/export

@app.get("/arms/exports/total")
async def arms_exports_total(country_code, year, currency):

    print('HERE', flush=True)
    if currency in VALID_CURRENCIES :
        query = sql.text(f'''select SUM("{currency}") from arms where "Source country" = :c and "Year" = :y;''')
        backup_query = sql.text(f'''select "{currency}" from exports where "Source country" = :c and "Year" = :y;''')
    else:
        return {'value': 'no data'}

    print(query)

    try:
        with db.connect() as conn:
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
        return {'value': 'no data'}



@app.get("/arms/exports/timeseries")
async def arms_exports_timeseries(country_code, currency):

    if currency in VALID_CURRENCIES:
        query = sql.text(f'''select coalesce (arms."Year", exports."Year"), coalesce (arms.sum, exports.sum) from
            (
            select "Year", SUM("{currency}") from arms
                            where "Source country" = :c
                            group by "Year"
                            order by "Year" asc
            ) as arms
            full outer join
            (
            select "Year", SUM("{currency}") from exports
            where "Source country" = :c
            group by "Year"
            order by "Year" asc
            ) as exports
            on arms."Year" = exports."Year" ;''')
    else:
        return {'value': 'no data'}

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'c': country_code})
            result = cursor.fetchall()

        if result == []:
            return {'value': 'no data'}

        return [{'year': year[0], 'value': int(year[1])} for year in result]

    except:
        return {'value': 'no data'}

# Gets export data for a country on a given year, listing values for source counries seperately
@app.get("/arms/exports/by_country")
async def arms_exports_by_country(country_code, year, currency, limit=300):
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

    if currency in VALID_CURRENCIES:
        query = sql.text(f'''select "Destination country", "{currency}", "short_name" from arms
            join country_names on "Destination country"="Alpha-2 code"
            where "Source country" = :c and "Year" = :y
            order by "{currency}" desc limit :l;''')
    else:
        return {'value': 'no data'}

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'c': country_code, 'y': year, 'l': limit})
            result = cursor.fetchall()

        if result == []:
            return {'value': 'no data'}

        return [{'name': country[0], 'value': country[1], 'full_name': country[2]} for country in result]
    except:
        return {'value': 'no data'}

# Gets the list of source countries that have any export data for a given
# year, so the frontend can grey out countries with nothing to show without
# a per-country round trip. Not currency-scoped: data presence doesn't
# depend on display currency. Always returns a bare array (empty if none),
# unlike the other endpoints above which return {'value': 'no data'}.
@app.get("/arms/exports/available")
async def arms_exports_available(year):

    query = sql.text('''select distinct "Source country" from arms where "Year" = :y
        union
        select distinct "Source country" from exports where "Year" = :y;''')

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'y': year})
            result = cursor.fetchall()

        return [country[0] for country in result if country[0] is not None]
    except:
        return []

# arms/import path endpoints

@app.get("/arms/imports/total")
async def arms_imports_total(country_code, currency, year):

    if currency in VALID_CURRENCIES:
        query = sql.text(f'''select SUM("{currency}") from arms where "Destination country" = :c and "Year" = :y;''')
    else:
        return {'value': 'no data'}

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'c': country_code, 'y': year})
            result = cursor.fetchall()

            # If aggregate function is used, result will not be empty, but NULL
            if result[0] == (None,):

                return {'value': 'no data'}

        return {'value': result[0][0]}
    except:
        return {'value': 'no data'}


@app.get("/arms/imports/by_country")
async def arms_imports_by_country(country_code, year, currency, limit=300):
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

    if currency in VALID_CURRENCIES:
        query = sql.text(f'''select "Source country", "{currency}", "short_name" from arms
        join country_names on "Source country"="Alpha-2 code"
        where "Destination country" = :c and "Year" = :y
        order by "{currency}" desc limit :l;''')
    else:
        return {'value': 'no data'}

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'c': country_code, 'v': currency, 'y': year, 'l': limit})
            result = cursor.fetchall()

        if result == []:
            return {'value': 'no data'}

        return [{'name': country[0], 'value': country[1], 'full_name': country[2]} for country in result]
    except:
        return {'value': 'no data'}

# Gets time series of total import values per year for a given country
@app.get("/arms/imports/timeseries")
async def arms_imports_timeseries(country_code, currency):

    if currency in VALID_CURRENCIES:

        query = sql.text(f'''select coalesce (arms."Year", imports."Year"), coalesce (arms.sum, imports.sum) from
            (
            select "Year", SUM("{currency}") from arms
                            where "Destination country" = :c
                            group by "Year"
                            order by "Year" asc
            ) as arms
            full outer join
            (
            select "Year", SUM("{currency}") from imports
            where "Destination country" = :c
            group by "Year"
            order by "Year" asc
            ) as imports
            on arms."Year" = imports."Year" ;''')
    else:
        return {'value': 'no data'}


    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'c': country_code})
            result = cursor.fetchall()

        if result == []:
            return {'value': 'no data'}

        return [{'year': year[0], 'value': int(year[1])} for year in result]

    except:
        return {'value': 'no data'}

# Gets the list of destination countries that have any import data for a
# given year - see /arms/exports/available above for why this shape (bare
# array, no currency param) differs from the other arms endpoints.
@app.get("/arms/imports/available")
async def arms_imports_available(year):

    query = sql.text('''select distinct "Destination country" from arms where "Year" = :y
        union
        select distinct "Destination country" from imports where "Year" = :y;''')

    try:
        with db.connect() as conn:
            cursor = conn.execute(query, parameters = {'y': year})
            result = cursor.fetchall()

        return [country[0] for country in result if country[0] is not None]
    except:
        return []


# Lambda entrypoint - translates between API Gateway's event/context shape
# and the ASGI interface FastAPI expects. Unused for local/container
# deployment (api.Dockerfile runs uvicorn directly against `app`).
handler = Mangum(app)
