# Passo1: Importar as bibliotecas

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

# Passo 2: Criar as funções de carregamento de dados
    # Cotações do Itau - ITUB4 - 2010 a 2024

@st.cache_data # Uma função do python que atribui uma funcionalidade para função logo embaixo dele
def carregar_dados(empresa):
    texto_tickers = " ".join(empresa)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-12-31")
    cotacoes_acao = cotacoes_acao["Close"]

    return cotacoes_acao

acoes = ["ITUB4.SA", "BBDC4.SA", "PETR4.SA", "VALE3.SA", "ABEV3.SA", "WEGE3.SA", "MGLU3.SA", "BBAS3.SA"]
dados = carregar_dados(acoes)
# Passo 3: Criar a interface do streamlit

st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
""") # Formato markdown

# Passo 4: Preparar as visualizações = filtros

st.sidebar.header("Filtros")

# filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns = {acao_unica: "Close"})

#filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período", min_value = data_inicial, max_value = data_final, value=(data_inicial, data_final), step = timedelta(days=30))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

# Criar o Gráfico
st.line_chart(dados)
