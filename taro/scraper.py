import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def democracy_index_scraper(out: str):
    url = 'https://en.wikipedia.org/w/index.php?title=The_Economist_Democracy_Index&oldid=1157018749'
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get all table rows represnting countries from the correct table (index 5)
    countries = soup.find_all('table')[5].find_all('tr')
    
    
    def get_country_data(country, columns):
    
        data = {}
        info = []
        
        # remove rank
        del columns[1]
        
        # remove region
        del columns[0]
        
        
        tds = country.find_all('td')
        
        
        try:
            tds[0]['id']
        except:
            tds = [None] + tds


        #info.append(tds[0].text.strip('\n'))
        
        # Country name
        info.append(tds[2].find('a').text)
        
        # Regime type
        info.append(tds[3].text.strip('\n'))
        
        # Values for years
        for td in tds[4:19]:
            info.append(float(td.text))
            
        for column, info in zip(columns, info):
            data[column.text.strip('\n')] = info
            
        return data
    
    table = []
    for country in countries[1:]:
    
        try:
            table.append(get_country_data(country, countries[0].find_all('th')))
        except:
            print(country)
            
    if out == 'csv':
        with open('data/democracy_index.csv', 'w') as file:
            writer = csv.DictWriter(file, fieldnames=table[0].keys())
            
            writer.writeheader()
            
            for row in table:
                writer.writerow(row)
    elif out == 'df' :
        return pd.DataFrame(table)
    else:
        raise ValueError("out needs to be one of ('csv', 'df')")