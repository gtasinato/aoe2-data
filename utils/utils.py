import requests
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
from harvester.models import Leaderboard
from django.utils import timezone as tz
from bs4 import BeautifulSoup as bs
from django.conf import settings



def harvest_leaderboard(base_url, id):
    game = 'aoe2de'
    name = '{date}_{code}_{leaderboard_id}.txt'.format(date=tz.now().strftime('%Y-%m-%d'),
                                    leaderboard_id=id, code=game)
    path = settings.MEDIA_ROOT + name

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
        request  = base_url.format(code=game, leaderboard_id=id, start=window_index, count=step)
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
                         top_player=data.name.iat[0],
                         game=game
                         )
    return result


def create_plot(leaderboard):
    if leaderboard.plot is not None:
        return leaderboard.plot

    # Change the file extension to .html
    file = '.'.join(leaderboard.csv_table.split('.')[:-1]) + '.html'
    df = pd.read_csv(leaderboard.csv_table)
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
#    print('Writing to html')
    fig.write_html(file, include_plotlyjs='cdn')
    print('Cleaning the output')
    with open(file, 'r') as f:
        soup = bs(f, 'html.parser')

    return str(soup.find('div'))


def compute_statistics(data):
    pass
