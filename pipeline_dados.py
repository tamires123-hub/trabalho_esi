import os
import pandas as pd
import numpy as np
import gdown
from kaggle.api.kaggle_api_extended import KaggleApi

def api_kaggle(datasets: list) -> None:
    api = KaggleApi()
    api.authenticate()
    os.makedirs('banco_de_dados', exist_ok=True)

    for df in datasets:
        api.dataset_download_files(
            df,
            path = 'banco_de_dados',
            unzip = True
        )
    return

def ler_df() -> list:
    datasets = os.listdir('banco_de_dados')
    dt = []
    for df in datasets:
        if df.endswith('.csv'):
            caminho = os.path.join('banco_de_dados', df)
            df = pd.read_csv(caminho)
            dt.append(df)
    return dt

def unir_df() -> None:
    dt = ler_df()
    dt[0]['names'] = dt[0]['Movie Name']

    filmes = pd.merge(dt[0], dt[1], on = 'names')
    filmes.to_csv('filmes.csv')

datasets = [
    'ashpalsingh1525/imdb-movies-dataset',
    'willianoliveiragibin/10000-data-about-movies-1915-2023'    
]

api_kaggle(datasets)
unir_df()