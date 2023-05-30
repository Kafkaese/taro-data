import src.scraper as sc

def test_democracy_index_scraper():
    df = sc.democracy_index()
    assert df.shape == (167, 17)
    assert (df.columns == ['Country', 'Regime type', '2022', '2021', '2020', '2019', '2018',
       '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2008',
       '2006']).sum() == 17
