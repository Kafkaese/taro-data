import psycopg2
from taro.scraper import democracy_index_scraper
import pandas as pd

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
    
def peace_index_pipe(source: str = 'csv', dest: str = 'postgres', **kwargs) -> bool:
    
    
    if source == 'csv':
        if 'csv_path' not in kwargs.keys():
            raise TypeError("If source = 'csv' is passed, keyword arguement csv_path is required")
        
        csv_path = kwargs['csv_path']
        
        peace_df = pd.read_csv(csv_path, header=3)
        
        # replace with corresponding pipe
        codes = pd.read_csv('../data/countries_info.csv', index_col=0)
        
        ''' 
        Gets dataframe with peace index values for years 2008 - 2022
        - merge on iso 3 country code column
        - select only first 21 columns, removes most of the irrelevant information
        -  drop remaining unneeded columns
        - set iso 2 country code as index
        '''
        peace_index_df = peace_df.merge(codes, left_on='iso3c', right_on='Alpha-3 code').iloc[:,:21].drop(columns = ['iso3c', 'Country','Country name', 'Official state name', 'Sovereignty']).set_index('Alpha-2 code')
    
