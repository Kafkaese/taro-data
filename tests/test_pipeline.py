from taro.pipeline import democracy_index_pipeline, country_code_pipeline
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os

conn_string = 'postgresql://postgres:password@localhost/postgres'

db = create_engine(conn_string)
conn = db.connect()
conn1 = psycopg2.connect(
    database="postgres",
    user='postgres', 
    password='password', 
    host='127.0.0.1', 
    port= '5432'
)

cursor = conn1.cursor()

def test_democracy_index_pipeline():
    
    democracy_index_pipeline(source='scraper', dest='postgres', db_conn = conn)
    
    # fetching all rows
    sql1='''select * from democracy_index;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='index')
    
    assert df.shape == (167, 17)
    assert (df.columns == ['Country', 'Regime type', '2022', '2021', '2020', '2019', '2018',
       '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2008',
       '2006']).sum() == 17

    
def test_country_code_pipeline():
    
    country_code_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path = os.path.join(os.path.dirname(__file__), '../data/iso_code_csv.csv'))
    
    # fetching all rows
    sql1='''select * from country_code;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='index')
    
    assert df.shape == (167, 17)
    assert (df.columns == ['Country', 'Regime type', '2022', '2021', '2020', '2019', '2018',
       '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2008',
       '2006']).sum() == 17

        
if __name__ == '__main__':
    test_democracy_index_pipeline()