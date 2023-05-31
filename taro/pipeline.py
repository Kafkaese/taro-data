import psycopg2
from taro.scraper import democracy_index_scraper

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