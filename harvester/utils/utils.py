import requests
import pandas as pd
from datetime import datetime
import os
import numpy as np
import plotly.graph_objects as go


def harvest_leaderboard(base_url, id):

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
    path = './not_versioned/data/{name}_{leaderboard_id}.{ext}'.format(name=datetime.now().strftime('%Y-%m-%d'), leaderboard_id=id, ext='txt')
    data.to_csv(path)
    print('Process completed!')

    return path

# TODO: write down subroutine to plot dataframe stored in csv file (leaderboard)
# def poltter(path):
#     data = pd.read_csv(path)
def create_plot(path):
    df = pd.read_csv(path)
    percentage = [np.around(np.mean(df.rating <= x)*100, 2) for x in df.rating]

    fig = go.Figure()

    fig.add_trace(go.Histogram(x=df.rating, hoverinfo = 'none'))
    fig.add_trace(go.Scatter(x=df.rating,
            y=percentage,
            hovertemplate='Elo: %{x:f}<br>' + 'In the best %{y:f}%<extra></extra>',
            mode="lines",
            opacity = 0
    ))

    fig.update_layout(barmode='overlay')
    fig.update_layout(hovermode='x unified')
    fig.update_layout(showlegend=False)

    return fig

def compute_statistics(data):
    pass
