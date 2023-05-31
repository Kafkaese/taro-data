from taro.pipeline import democracy_index_pipeline

from sqlalchemy import create_engine
import psycopg2

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
    cursor.execute(sql1)
    for i in cursor.fetchall():
        print(i)
        
if __name__ == '__main__':
    test_democracy_index_pipeline()