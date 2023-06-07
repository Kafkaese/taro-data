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
    
def peace_index_pipe(source: str = 'csv', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets peace index data from 'source' and writes to 'dest'

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
        
        peace_df = pd.read_csv(csv_path, header=3)
        
        # replace with corresponding pipe
        codes = pd.read_csv(os.path.join(os.path.dirname(__file__),'../data/countries_info.csv'), index_col=0)
        
        ''' 
        Gets dataframe with peace index values for years 2008 - 2022
        - merge on iso 3 country code column
        - select only first 21 columns, removes most of the irrelevant information
        -  drop remaining unneeded columns
        - set iso 2 country code as index
        '''
        peace_df = peace_df.merge(codes, left_on='iso3c', right_on='Alpha-3 code').loc[:,['Alpha-2 code', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
       '2017', '2018', '2019', '2020', '2021', '2022']].set_index('Alpha-2 code')

    if dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        peace_df.to_sql('peace_index', db_conn, if_exists='replace')

    else:
        pass
    
def country_info_pipeline(source: str = 'csv', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets counrty info data from 'source' and writes to 'dest'
    
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
        
        code_df = pd.read_csv(csv_path, header=0, index_col=0)
        
        
    if dest == 'postgres':
        
        print(code_df)
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        code_df.to_sql('country_info', db_conn, if_exists='replace')

    else:
        pass
    