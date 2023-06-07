import psycopg2
from taro.scraper import democracy_index_scraper
import pandas as pd
import os

def democracy_index_pipeline(source: str = 'scraper', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets democracy index data from source and writes to dest.
    
    Keyword arguments:
    source -- either one of ('scraper', 'csv')
    dest -- either one of ('postgres', 'csv')
    
    db_conn -- postgres database connection. Only if dest = 'postgres'
    csv_src_path -- path to source csv file. Only if source = 'csv'
    csv_dest_path -- path to destination csv. Only if dest = 'csv'

    Returns:
    0 if data was successfully written to dest, 1 if not
    '''    
    # Run scraper
    if source == 'scraper':
        data = democracy_index_scraper('df')

    if dest == 'csv':
        data.to_csv('../data/dem_id_TEST.csv')
    
    elif dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        data.to_sql('democracy_index', db_conn, if_exists='replace')

    else:
        pass
    
def country_code_pipeline(source: str = 'csv', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets counrty code data from 'source' and writes to 'dest'
    
    Keyword arguments:
    source -- either one of ('csv')
    dest -- either one of ('postgres', 'csv')
    
    db_conn -- postgres database connection. Only if dest = 'postgres'
    csv_src_path -- path to source csv file. Only if source = 'csv'
    csv_dest_path -- path to destination csv. Only if dest = 'csv'

    Returns:
    0 if data was successfully written to dest, 1 if not
    
    '''

    if source == 'csv':
        if 'csv_path' not in kwargs.keys():
            raise TypeError("If source = 'csv' is passed, keyword arguement csv_path is required")
        
        csv_path = kwargs['csv_path']
        
        code_df = pd.read_csv(csv_path, header=1)
        
        
    if dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        code_df.to_sql('country_code', db_conn, if_exists='replace')

    else:
        pass