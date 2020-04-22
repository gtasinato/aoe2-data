import requests
import pandas as pd
from datetime import datetime
import os

def harvest_leaderboard(base_url):

    window_index = 1
    step = 1000
    data = pd.DataFrame()

    print('Parameters set. Starting the harvesting')
    while True:
        print('Collecting entries from {} to {}'.format(window_index, window_index + step -1))
        request  = base_url.format(start=window_index, count=step)
        raw = requests.get(request).json()
        print('Request handeled. Converting to pandas DataFrame.')
        aux = pd.DataFrame(raw['leaderboard'])
        print('Conversion completed. Merging the dataset')
        if not aux.empty:
            window_index = window_index + step
            data = data.append(aux, ignore_index=True, sort=False)
            print('Process completed. Starting the analysis of next batch...')
        else:
            print('Data harvested!')
            break
    print('Zipping the dataset...')
    data.to_csv('./not_versioned/data/{name}.{ext}'.format(name=datetime.now().strftime('%Y-%m-%d'), ext='txt'))
    print('Process completed!')

    return

# TODO: write down subroutine to plot dataframe stored in csv file (leaderboard)
# def poltter(path):
#     data = pd.read_csv(path)
