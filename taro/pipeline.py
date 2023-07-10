import psycopg2
from sqlalchemy import create_engine, types
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
    elif source == 'csv':
        if 'csv_path' not in kwargs.keys():
            raise TypeError("If source = 'csv' is passed, keyword arguement csv_path is required")
        
        csv_path = kwargs['csv_path']
        
        data = pd.read_csv(csv_path, header=0)
    
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
    
def import_data_pipeline(source: str = 'csv', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets export data from 'source' and writes to 'dest'
    
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
        
        imports_df = pd.read_csv(csv_path, header=0, index_col=0)
        
        
    if dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        imports_df.to_sql('imports', db_conn, if_exists='replace',dtype= {'Destination country': types.VARCHAR, 'Year': types.INTEGER, 'Value' : types.BIGINT})

    else:
        pass
    
def export_data_pipeline(source: str = 'csv', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets export data from 'source' and writes to 'dest'
    
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
        
        export_df = pd.read_csv(csv_path, header=0, index_col=0)
        
        
    if dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        export_df.to_sql('exports', db_conn, if_exists='replace', dtype={'Source country': types.VARCHAR, 'Year': types.INTEGER, 'Value' : types.BIGINT})

    else:
        pass
    
def country_name_pipeline(source: str = 'scraper', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets cpuntry name data from source and writes to dest.
    
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
    
    if source == 'csv':
        if 'csv_path' not in kwargs.keys():
            raise TypeError("If source = 'csv' is passed, keyword arguement csv_path is required")
        
        csv_path = kwargs['csv_path']
        
        data = pd.read_csv(csv_path, header=0, index_col=0)
    
    if dest == 'csv':
        data.to_csv('../data/dem_id_TEST.csv')
    
    elif dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        data.to_sql('country_names', db_conn, if_exists='replace')

    else:
        pass
    
def merch_export_pipeline(source: str = 'scraper', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets total merchandise export data from source and writes to dest.
    
    Keyword arguments:
    source -- either one of ('scraper', 'csv')
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
        
        data = pd.read_csv(csv_path, header=0, index_col=0)
    
    
    if dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        data.to_sql('merchandise_exports', db_conn, if_exists='replace')

    else:
        pass
    
def arms_pipeline(source: str = 'scraper', dest: str = 'postgres', **kwargs) -> bool:
    '''
    Gets total arms export and import for all years data from source and writes to dest.
    
    Keyword arguments:
    source -- either one of ('scraper', 'csv')
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
        
        data = pd.read_csv(csv_path, header=0, index_col=0)
    
    
    if dest == 'postgres':
        
        if 'db_conn' not in kwargs.keys():
            raise TypeError("If dest = 'postgres' is passed, keyword arguement db_conn is required")
        
        db_conn = kwargs['db_conn']

        data.to_sql('arms', db_conn, if_exists='replace')

    else:
        pass
       
if __name__ == "__main__":

    # Connection string info
    
    host = os.environ['POSTGRES_HOST']
    dbname = os.environ['POSTGRES_DB']
    
    # Use tf vars if not local dev env
    if os.environ['ENV'] == 'dev':
        user = os.environ['POSTGRES_USER']
        password = os.environ['POSTGRES_PASSWORD']
    else:    
        user = os.environ['TF_VAR_postgres_user']
        password = os.environ['TF_VAR_postgres_password']
    
    sslmode = "require"
    
    # Construct connection string
    print(f"USING ENV: {os.environ['ENV']}")
    conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{5432}/{dbname}"
    
    print(conn_string)
    
    # Create connection
    db = create_engine(conn_string)
    conn = db.connect()

 
    # Run all pipelines
    
    import_data_pipeline(db_conn = conn, csv_path = '../data/imports.csv')
    
    export_data_pipeline(db_conn = conn, csv_path = '../data/exports.csv')
    
    democracy_index_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path='../data/democracy_index.csv')
    
    peace_index_pipe(source='csv', dest='postgres', csv_path=os.path.join(os.path.dirname(__file__),'../raw_data/GPI-2022-overall-scores-and-domains-2008-2022.csv'), db_conn=conn)
    
    merch_export_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path='../data/total_merchandise_exports.csv')
    
    arms_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path = '../data/arms.csv')
    
    country_name_pipeline(source='csv', dest='postgres', db_conn = conn, csv_path = '../data/countries_info.csv')