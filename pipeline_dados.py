def main():
    import os
    import pandas as pd
    import numpy as np
    import requests
    import re
    from kaggle.api.kaggle_api_extended import KaggleApi

    # Fatores de correção da inflação
    FATORES_IPCA = {
        2010: 2.03, 2011: 1.92, 2012: 1.81, 2013: 1.71, 2014: 1.61,
        2015: 1.45, 2016: 1.31, 2017: 1.23, 2018: 1.19, 2019: 1.14,
        2020: 1.09, 2021: 1.00, 2022: 0.94, 2023: 0.90, 2024: 0.86, 2025: 1.00
    }

    datasets = [
        'ashpalsingh1525/imdb-movies-dataset',
        'willianoliveiragibin/10000-data-about-movies-1915-2023'    
    ]

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

    def carregar_e_filtrar_dados(caminho_csv):
        df = pd.read_csv(caminho_csv)
        df = df[df['Year of Release'] >= 2010]
        df = df.dropna(subset=["revenue"])
        return df

    def ajustar_inflacao_e_calcular_lucro(df):
        df["fator_ipca"] = df["Year of Release"].map(FATORES_IPCA)
        df["lucro"] = (df["revenue"] - df["budget_x"]) / df["fator_ipca"]
        df["budget_x"] = df["budget_x"] / df["fator_ipca"]
        return df

    def tratar_nomes_direcao_e_elenco(df):
        df['diretor'] = df['Director'].apply(lambda x: re.sub(r"[\[\]']", "", str(x)))

        def tratar_crew(x):
            if isinstance(x, list):
                return [i.strip() for i in x if isinstance(i, str) and i.strip()]
            elif isinstance(x, str):
                return [i.strip() for i in x.strip("[]").split(",") if i.strip()]
            return []

        df['crew'] = df['crew'].fillna("").apply(tratar_crew)
        df['diretor'] = df['diretor'].fillna("").apply(tratar_crew)
        return df

    def calcular_notas_media_mediana(df):
        def limpar_nome(nome):
            return nome.strip(' "\'')

        # Notas dos atores
        df_atores = df[['crew', 'Movie Rating']].copy()
        df_atores['crew'] = df_atores['crew'].astype(str).str.split(',')
        df_atores = df_atores.explode('crew')
        df_atores['crew'] = df_atores['crew'].str.strip()
        notas_atores = df_atores.groupby('crew')['Movie Rating'].mean().to_dict()

        # Notas dos diretores
        df_diretores = df[['diretor', 'Movie Rating']].copy()
        df_diretores['diretor'] = df_diretores['diretor'].astype(str).str.split(',')
        df_diretores = df_diretores.explode('diretor')
        df_diretores['diretor'] = df_diretores['diretor'].str.strip()
        notas_diretores = df_diretores.groupby('diretor')['Movie Rating'].mean().to_dict()

        # Limpeza dos nomes
        remover = "[]{}'\" "
        notas_atores = {k.strip(remover): v for k, v in notas_atores.items()}
        notas_diretores = {k.strip(remover): v for k, v in notas_diretores.items()}

        def calcular_nota(lista, notas_dict):
            notas = [notas_dict[n] for n in lista if n in notas_dict]
            return [np.mean(notas) if notas else 0, np.median(notas) if notas else 0]

        df['media_elenco'] = df['crew'].apply(lambda l: calcular_nota(l, notas_atores)[0])
        df['mediana_elenco'] = df['crew'].apply(lambda l: calcular_nota(l, notas_atores)[1])
        df['media_direcao'] = df['diretor'].apply(lambda l: calcular_nota(l, notas_diretores)[0])
        df['mediana_direcao'] = df['diretor'].apply(lambda l: calcular_nota(l, notas_diretores)[1])
        return df

    def codificar_generos(df):
        df['genre'] = df['genre'].fillna("").astype(str)
        df['genre'] = df['genre'].apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
        
        todos_generos = list(set(g for sublist in df['genre'] for g in sublist))
        for genero in todos_generos:
            df[genero] = df['genre'].apply(lambda lista: 1 if genero in lista else 0)
        return df

    def engenhar_temporais(df):
        df['date_x'] = pd.to_datetime(df['date_x'])
        df['mes'] = df['date_x'].dt.month
        df['mes_sin'] = np.sin(2 * np.pi * df['mes'] / 12)
        df['mes_cos'] = np.cos(2 * np.pi * df['mes'] / 12)
        return df

    def categorizar_lucro(df):
        q2 = df['lucro'].quantile(0.66)
        bins = [-float('inf'), 0, q2, float('inf')]
        labels = ['Prejuízo', 'Lucro baixo', 'Lucro alto']
        df['categoria_lucro'] = pd.cut(df['lucro'], bins=bins, labels=labels)
        return df

    def selecionar_e_renomear_colunas(df):
        colunas_usadas = [
            'Year of Release', 'mes_sin', 'mes_cos', 'Run Time in minutes', 'budget_x',
            'media_elenco', 'media_direcao', 'mediana_elenco', 'mediana_direcao',
            'Drama', 'Mystery', 'Action', 'Family', 'Documentary', 'Crime', 'Romance',
            'War', 'Comedy', 'Fantasy', 'Adventure', 'Thriller', 'Science Fiction',
            'Western', 'History', 'Horror', 'Animation', 'Music', 'TV Movie',
            'categoria_lucro'
        ]
        df = df[colunas_usadas].copy()
        df = df.rename(columns={
            'Year of Release': 'ano_lancamento',
            'mes_sin': 'mes_seno',
            'Run Time in minutes': 'duracao',
            'budget_x': 'orcamento'
        })
        return df

    def tratar_dados(df):
        colunas = ['duracao', 'orcamento', 'media_elenco', 'media_direcao', 'mediana_elenco', 'mediana_direcao']
        for coluna in colunas:
            df = df[df[coluna] != 0]
        return df.dropna()

    # Pipeline principal
    api_kaggle(datasets)
    unir_df()

    df = carregar_e_filtrar_dados("filmes.csv")
    df = ajustar_inflacao_e_calcular_lucro(df)
    df = tratar_nomes_direcao_e_elenco(df)
    df = calcular_notas_media_mediana(df)
    df = codificar_generos(df)
    df = engenhar_temporais(df)
    df = categorizar_lucro(df)
    df = selecionar_e_renomear_colunas(df)
    df = tratar_dados(df)

    df_oficial = df.copy()
    # Salva o dataframe completo com todas as colunas criadas ao longo do pipeline
    # Útil para análises exploratórias ou como backup geral
    df.to_csv("filmes_final_completo.csv", index=False)

    # Salva o dataframe tratado e reduzido, pronto para modelagem (df_oficial)
    # Esse é o dataset final que será usado em tarefas de classificação
    df_oficial.to_csv("dataset_filmes_class.csv", index=False)

    print(len(df_oficial), df_oficial.head())

if __name__ == "__main__":
    main()
