# -*- coding: utf-8 -*-
"""trabalho_Org_de_Dados.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GhzzFPg6_5Jur6kbezcVOVF8t5mwmLT3
"""


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud


try:
  df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQd3Uv6rDQcZXGCUAXhuKhrad6dhLZ6Tdmv-0AVFlNIizd_AjJ-1djBNa-dlMlB-ZvH5mbl7hf5vWsd/pub?gid=848950540&single=true&output=csv')
except:
  #Em caso de sem internet
  df = pd.read_csv('imdb_top_1000.csv')

# Agrupar por gênero e calcular a média do IMDB_Rating
genero_notas_IMDB = df.assign(Genre=df['Genre'].str.split(',')).explode('Genre').groupby('Genre')['IMDB_Rating'].agg('mean').sort_values(ascending=False)
genero_notas_Meta = df.assign(Genre=df['Genre'].str.split(',')).explode('Genre').groupby('Genre')['Meta_score'].agg('mean').sort_values(ascending=False)


# Função para gerar o histograma de notas do IMDB
def plot_imdb_histogram():
    fig, ax = plt.subplots()
    ax.hist(df['IMDB_Rating'], bins=10, edgecolor='black')
    ax.set_xlabel('IMDB Rating')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Função para gerar o histograma de notas do Meta Score
def plot_meta_score_histogram():
    fig, ax = plt.subplots()
    ax.hist(df['Meta_score'], bins=10, edgecolor='black')
    ax.set_xlabel('Meta Score')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Função para gerar o gráfico de barras de gêneros
def plot_genre_wordcloud():
    generos = df['Genre'].str.split(',').explode().str.strip().value_counts()
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(generos)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def plot_runtime_bar_chart():
    # 1. Extraindo os números da coluna "Runtime"
    runtime_data = df['Runtime'].str.extract('(\d+)').astype(int)

    # 2. Criando o histograma
    fig, ax = plt.subplots()  # Cria a figura e o eixo
    ax.hist(runtime_data, bins=12, edgecolor='black')  # Cria o histograma
    ax.set_title('Distribuição de Duração dos Filmes')
    ax.set_xlabel('Duração (minutos)')
    ax.set_ylabel('Quantidade de Filmes')
    st.pyplot(fig)  # Exibe a figura no Streamlit

# Interface do Streamlit
st.title("Dashboard Interativo de Filmes")

# Sidebar com opções
st.sidebar.title("Opções")
analysis_type = st.sidebar.selectbox("Selecione a Análise", ["Visão Geral","Classificação Indicativa", "Notas IMDB", "Meta Score", "Gêneros", "Tempo dos filmes", "Resumo"])

# Conteúdo do dashboard com base na seleção
if analysis_type == "Visão Geral":
  st.header("Visão Geral do Dataset")
  st.write(df.head())
  st.write(df.describe())
  st.write(df.info())
  st.write(df.isnull().sum())
    
  st.write("Usamos Dados Brutos (criando até dados Agregados no momento de médias) e Dados secundários tirados de: https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows/data e Dados Estruturados")

# Momento de tirar os 'is null' desse data frame na visão de dados medianas ou strings demonstrando que não foi informado
df['Certificate'].fillna('Não informado')

# Fazendo uma variável para armazenar a receita bruta na forma de inteiro (já que veio no dataset em str com virgulas separando)
Novo_Gross = pd.to_numeric(df['Gross'].str.replace(',', ''), errors='coerce')

# Fazendo a mediana (agora que podemos fazer depois de tirar de str para float)
mediana_gross = Novo_Gross.median()

# Trocando os com Gross NaN pela mediana_gross
Novo_Gross.fillna(mediana_gross, inplace=True)

# Fazendo nossa coluna do Gross pela nova coluna com inteiros!
df['Gross'] = Novo_Gross

# Código para trocar os valores nulos em Meta_score pela mediana
# Verificando se há valores nulos na coluna 'Meta_score' e contando-os
valores_nulos = df['Meta_score'].isnull().sum()

# Calculando a mediana da coluna 'Meta_score' (excluindo valores nulos)
mediana_meta_score = df['Meta_score'].dropna().median()

# Preenchendo os valores nulos com a mediana
df.fillna({'Meta_score' : mediana_meta_score}, inplace=True)



if analysis_type == "Classificação Indicativa":
  # Agrupar e contar as ocorrências de cada certificado
  certificados = df['Certificate'].value_counts()

  # Criar a wordcloud
  wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(certificados)

  # Exibir a wordcloud no Streamlit
  fig, ax = plt.subplots()
  ax.imshow(wordcloud, interpolation='bilinear')
  ax.axis("off")
  st.pyplot(fig)

elif analysis_type == "Notas IMDB":
  st.header("Análise das Notas do IMDB")
  plot_imdb_histogram()
  st.write("O filme com maior nota IMDB é:" + str(df['Series_Title'][df['IMDB_Rating'] == df['IMDB_Rating'].max()].values[0]) + " sendo sua nota de: " + str(df['IMDB_Rating'][df['IMDB_Rating'] == df['IMDB_Rating'].max()].values[0]))
  st.write("O filme com menor nota IMDB é:" + str(df['Series_Title'][df['IMDB_Rating'] == df['IMDB_Rating'].min()].values[0]) + " sendo sua nota de: " + str(df['IMDB_Rating'][df['IMDB_Rating'] == df['IMDB_Rating'].min()].values[0]))

elif analysis_type == "Meta Score":
  st.header("Análise do Meta Score")
  plot_meta_score_histogram()
  st.write("O filme com maior nota Meta Score é: " + str(df['Series_Title'][df['Meta_score'] == df['Meta_score'].max()].values[0]) + " sendo sua nota de: " + str(df['Meta_score'][df['Meta_score'] == df['Meta_score'].max()].values[0]))
  st.write("O filme com menor nota Meta Score é: " + str(df['Series_Title'][df['Meta_score'] == df['Meta_score'].min()].values[0]) + " sendo sua nota de: " + str(df['Meta_score'][df['Meta_score'] == df['Meta_score'].min()].values[0]))

elif analysis_type == "Gêneros":
  generos = df['Genre'].str.split(',').explode().str.strip().value_counts()
  st.header("Análise de Gêneros")
  plot_genre_wordcloud()
  
  # Gráfico de barras para genero_notas_IMDB
  st.subheader("Nota Média do IMDB por Gênero")  # Título do gráfico
  fig, ax = plt.subplots(figsize=(10, 6))  # Cria a figura e os eixos
  ax.bar(genero_notas_IMDB.index, genero_notas_IMDB.values)
  ax.set_xlabel("Gêneros")
  ax.set_ylabel("Nota Média do IMDB")
  ax.set_xticklabels(genero_notas_IMDB.index, rotation=45, ha='right')  # Rotaciona os rótulos do eixo x
  st.pyplot(fig)  # Exibe o gráfico no Streamlit

  # Gráfico de barras para genero_notas_Meta
  st.subheader("Nota Média do Meta Score por Gênero")  # Título do gráfico
  fig, ax = plt.subplots(figsize=(10, 6))  # Cria a figura e os eixos
  ax.bar(genero_notas_Meta.index, genero_notas_Meta.values)
  ax.set_xlabel("Gêneros")
  ax.set_ylabel("Nota Média do Meta Score")
  ax.set_xticklabels(genero_notas_Meta.index, rotation=45, ha='right')  # Rotaciona os rótulos do eixo x
  st.pyplot(fig)  # Exibe o gráfico no Streamlit
  st.write("O Gênero mais comum é: " + str(generos.index[0]))
  st.write("O Gênero mais raro é: " + str(generos.index[len(generos)-1]))

elif analysis_type == "Tempo dos filmes":
  Nova_coluna = df['Runtime'].str.extract('(\d+)').astype(int)
  i_max = int(Nova_coluna.idxmax())
  i_min = int(Nova_coluna.idxmin())
  st.header("Análise do Tempo dos Filmes")
  plot_runtime_bar_chart()
  st.write("O Filme com maior tempo é: " + str(df.loc[i_max,'Series_Title']) + ' e seu tempo é de: ' + str(Nova_coluna.max()[0]))
  st.write("O Filme com menor tempo é: " + str(df.loc[i_min,'Series_Title']) + ' e seu tempo é de: ' + str(Nova_coluna.min()[0]))

elif analysis_type == "Resumo":
  st.header("Resumo")
  st.write("A maioria dos filmes tem notas no IMDB entre 7.5 e 8.5, com poucos filmes acima de 8.75. Isso sugere uma distribuição concentrada na faixa de bom a ótimo.")
  st.write("A classificação indicativa que mais ocorre é: ")
  st.write("A distribuição do Meta Score é diferente, com a maioria dos filmes entre 60 e 90, sendo difícil encontrar filmes acima de 90 ou abaixo de 55. Essa diferença na distribuição pode refletir critérios de avaliação distintos entre o público (IMDB) e os críticos (Meta Score).")
  st.write("As notas do IMDB e Meta Score podem ser comparadas para identificar filmes que foram bem recebidos tanto pelo público quanto pela crítica, ou que tiveram avaliações divergentes.")
  st.write("O gênero mais frequente no dataset é Drama, seguido por outros gêneros populares como Ação, Crime e Comédia.")
  st.write("A maioria dos filmes tem duração entre 100 e 200 minutos.")
  st.write("Além disso, mudamos as classificações indicativas que estavam vazias para 'Não informado'")
