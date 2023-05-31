from taro.pipeline import democracy_index_pipeline

from sqlalchemy import create_engine
import psycopg2

conn_string = 'postgresql://postgres:password@127.0.0.1/postgres'

db = create_engine(conn_string)
conn = db.connect()
conn1 = psycopg2.connect(
    database="postgres",
    user='postgres', 
    password='password', 
    host='127.0.0.1', 
    port= '5432'
)
