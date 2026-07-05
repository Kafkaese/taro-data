from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Pinned to a specific historical revision so the parsing logic doesn't
# unexpectedly break when Wikipedia's page changes underneath it. Re-pin
# this to a newer oldid once a year when the Economist publishes fresh
# Democracy Index data - and when you do, regenerate
# tests/fixtures/democracy_index.html to match (see test_scraper.py). The
# table layout has shifted across past revisions, so re-pinning may also
# require adjusting parse_democracy_index_html, not just the URL.
DEMOCRACY_INDEX_URL = 'https://en.wikipedia.org/w/index.php?title=The_Economist_Democracy_Index&oldid=1157018749'


def fetch_democracy_index_html(url: str = DEMOCRACY_INDEX_URL):
    # Plain `requests` gets a 403 here even with a descriptive User-Agent -
    # Wikimedia's anti-bot layer fingerprints the TLS/HTTP handshake itself,
    # and requests' (urllib3's) handshake is a well-known bot signature
    # regardless of headers. curl_cffi makes the request with a real
    # browser's TLS fingerprint instead, while keeping a requests-like API.
    response = requests.get(url, impersonate="chrome")
    return response.content


def parse_democracy_index_html(html):
    soup = BeautifulSoup(html, 'html.parser')

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

        # Most rows have 18 <td>s: rank, country, regime type, 15 years.
        # Rows that happen to be first in their region group have a 19th,
        # leading <td> for the region (Wikipedia renders it once per group
        # via rowspan, not on every row). Detecting that via an id
        # attribute (as this used to) doesn't work against Parsoid-rendered
        # pages, which stamp an id onto every cell regardless - the actual
        # cell count is a reliable signal, the id's presence isn't.
        if len(tds) == 18:
            tds = [None] + tds

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

    return table


def democracy_index_scraper(out: str):
    html = fetch_democracy_index_html()
    table = parse_democracy_index_html(html)

    if out == 'csv':
        with open('data/democracy_index.csv', 'w') as file:
            writer = csv.DictWriter(file, fieldnames=table[0].keys())

            writer.writeheader()

            for row in table:
                writer.writerow(row)
    elif out == 'df':
        return pd.DataFrame(table)
    else:
        raise ValueError("out needs to be one of ('csv', 'df')")
