
from taro.pipeline import democracy_index_pipeline, peace_index_pipe, country_code_pipeline, country_info_pipeline
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os

if os.environ['ENV'] == 'dev':
    conn_string = 'postgresql://postgres:password@localhost/postgres'
elif os.environ['ENV'] == 'test':
    pass
else:
    host = "taro-server.postgres.database.azure.com"
    dbname = "taro-db"
    user = "postgres"
    password = os.environ['POSTGRES_PASSWORD']
    sslmode = "require"
    conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{5432}/{dbname}"


db = create_engine(conn_string)
conn = db.connect()

def test_democracy_index_pipeline():
    
    democracy_index_pipeline(source='scraper', dest='postgres', db_conn = conn)
    
    # fetching all rows
    sql1='''select * from democracy_index;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='index')
    
    assert df.shape == (167, 17)
    assert (df.columns == ['Country', 'Regime type', '2022', '2021', '2020', '2019', '2018',
       '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2008',
       '2006']).sum() == 17

def test_peace_index_pipe():
    peace_index_pipe(source='csv', dest='postgres', csv_path=os.path.join(os.path.dirname(__file__),'../raw_data/GPI-2022-overall-scores-and-domains-2008-2022.csv'), db_conn=conn)
    
    # fetching all rows
    sql1='''select * from peace_index;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='Alpha-2 code')
    
    assert list(df.columns) == ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
       '2017', '2018', '2019', '2020', '2021', '2022']
    assert df.sum().sum() == 4919.357

    
    #country_code_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path = os.path.join(os.path.dirname(__file__), '../data/iso_code_csv.csv'))
    
    # fetching all rows
    sql1='''select * from peace_index;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='Alpha-2 code')
    
    assert df.shape == (162, 16)

def test_country_code_pipeline():
    
    country_code_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path = os.path.join(os.path.dirname(__file__), '../data/iso_code_csv.csv'))
    
    # fetching all rows
    sql1='''select * from country_code;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='index')
    
    assert df.shape == (248, 2)

def test_country_info_pipeline():
    
    country_info_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path = os.path.join(os.path.dirname(__file__), '../data/countries_info.csv'))
    
    # fetching all rows
    sql1='''select * from country_info;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='index')
    
    assert df.shape == (271, 8)
        
if __name__ == '__main__':
    test_democracy_index_pipeline()