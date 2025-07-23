import os
import pandas as pd
import numpy as np
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

def lendo_df():
    datasets = os.listdir('banco_de_dados')
    dt = {}
    for df in datasets:
        caminho = os.path.join('banco_de_dados', df)
        df = pd.read_csv(caminho)
        nome = os.path.splitxt(df)[0]
        dt[nome] = df

    return dt

datasets = [
    '/ashpalsingh1525/imdb-movies-dataset',
    '/willianoliveiragibin/10000-data-about-movies-1915-2023'
]

