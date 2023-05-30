import psycopg2
from taro.scraper import democracy_index

def democracy_index(source: str = 'scraper', dest: str = 'postgres') -> None:
    
    # Run scraper
    if source == 'scraper':
        data = democracy_index()

    if dest == 'csv':
        data.to_csv('../data/dem_id_TEST.csv')
    elif dest == 'postgres':
        pass