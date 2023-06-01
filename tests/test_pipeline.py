from taro.pipeline import democracy_index_pipeline, peace_index_pipe
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

    
def test_peace_index_pipe():
    peace_index_pipe(source='csv', dest='postgres', csv_path=os.path.join(os.path.dirname(__file__),'../data/GPI-2022-overall-scores-and-domains-2008-2022.csv'), db_conn=conn)
    
    # fetching all rows
    sql1='''select * from peace_index;'''
    
    df = pd.read_sql_query(sql1, conn, index_col='Alpha-2 code')
    
    assert df.sum().sum() == 4919.357
    
        
if __name__ == '__main__':
    test_democracy_index_pipeline()