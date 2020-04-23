import requests
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
from ..models import Leaderboard
from django.utils import timezone as tz
from bs4 import BeautifulSoup as bs


def harvest_leaderboard(base_url, id):
    name = '{date}_{leaderboard_id}.txt'.format(date=tz.now().strftime('%Y-%m-%d'),
                                    leaderboard_id=id)
    path = './not_versioned/data/'+ name

# if database entry already exists, just return it, else create it
    query =  Leaderboard.objects.filter(csv_table__contains=name)
    if query:
        result = query.get()
        return result

    window_index = 1
    step = 10000
    data = pd.DataFrame()

    print('Parameters set. Starting the harvesting')
    while True:
        print('Collecting entries from {} to {}'.format(window_index, window_index + step -1))
        request  = base_url.format(leaderboard_id=id, start=window_index, count=step)
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
    data.to_csv(path)
    print('Process completed!')
    result = Leaderboard.objects.create(leaderboard_id=id,
                         date=tz.now(),
                         csv_table=path,
                         population=len(data.index),
                         average_elo=data.rating.mean(),
                         top_player=data.name.iat[0]
                         )
    return result

# TODO: write down subroutine to plot dataframe stored in csv file (leaderboard)
# def poltter(path):
#     data = pd.read_csv(path)
def create_plot(leaderboard):
    if leaderboard.plot is not None:
        return leaderboard.plot

    df = pd.read_csv(leaderboard.csv_table)
    print(df.head())
    titles = {
              0 : 'Unranked',
              1 : 'Deathmatch 1v1',
              2 : 'Team Deathmatch',
              3 : 'Random Map 1v1',
              4 : 'Team Random Map'
              }
    percentage = [np.around(np.mean(df.rating <= x)*100, 2) for x in df.rating]
    print('Start Plotting')
    fig = go.Figure()

    fig.add_trace(go.Histogram(x=df.rating, hoverinfo = 'none'))
    fig.add_trace(go.Scatter(x=df.rating,
            y=percentage,
            hovertemplate='Elo: %{x:f}<br>' + 'In the best %{y:f}%<extra></extra>',
            mode="lines",
            opacity = 0
    ))
    print('Updating layout')
    fig.update_layout(barmode='overlay')
    fig.update_layout(hovermode='x unified')
    fig.update_layout(showlegend=False)
    fig.update_layout(title = titles[leaderboard.leaderboard_id])
    print('Writing to html')
    fig.write_html('not_versioned/test.html', include_plotlyjs='cdn')
    print('Cleaning the output')
    with open('not_versioned/test.html', 'r') as f:
        soup = bs(f, 'html.parser')

    return str(soup.find('div'))


def compute_statistics(data):
    pass
