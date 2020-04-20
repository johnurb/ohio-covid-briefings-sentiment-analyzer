#! usr/bin/env python3
'''
Pull down the New York Times' csv of COVID data from their github repo
'''
import pandas as pd
from datetime import datetime
import requests
import io

'''
Function to pull down the NYT csv
Returns an IO object that can be read into the Pandas 'read_csv' method
'''
def get_stats():
    csv_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    csv_r = requests.get(csv_url).content
    data = pd.read_csv(io.BytesIO(csv_r), parse_dates=['date'])
    data.columns = data.columns.str.title()
    del data['Fips']
    data = data[data['State'] == 'Ohio'].reset_index(drop=True)
    del data['State']

    return data

if __name__ == '__main__':
    print(get_stats())
