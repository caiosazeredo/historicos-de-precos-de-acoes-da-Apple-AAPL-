import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pandas_datareader import data as pdr

# Definindo o período da análise
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2021, 1, 1)

# Carregando dados de ações do Yahoo Finance
ticker = 'AAPL'
df = pdr.get_data_yahoo(ticker, start_date, end_date)

# Calculando retornos diários
df['Daily Returns'] = df['Adj Close'].pct_change()

# Calculando médias móveis de 20 e 50 dias
df['MA20'] = df['Adj Close'].rolling(window=20).mean()
df['MA50'] = df['Adj Close'].rolling(window=50).mean()

# Calculando a volatilidade (desvio padrão dos retornos diários) em uma janela móvel de 20 dias
df['Volatility'] = df['Daily Returns'].rolling(window=20).std() * np.sqrt(20)

# Função para plotar os dados
def plot_data(df, title='Análise Quantitativa Computacional'):
    fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    # Preço ajustado de fechamento
    axs[0].plot(df.index, df['Adj Close'], label='Preço Ajustado')
    axs[0].plot(df.index, df['MA20'], label='Média Móvel 20 Dias', linestyle='--')
    axs[0].plot(df.index, df['MA50'], label='Média Móvel 50 Dias', linestyle='--')
    axs[0].set_ylabel('Preço')
    axs[0].set_title(title)
    axs[0].legend()

    # Retornos diários
    axs[1].plot(df.index, df['Daily Returns'], label='Retornos Diários', color='orange')
    axs[1].set_ylabel('Retorno Diário')
    axs[1].axhline(0, color='black', linewidth=1)
    axs[1].legend()

    # Volatilidade
    axs[2].plot(df.index, df['Volatility'], label='Volatilidade', color='green')
    axs[2].set_ylabel('Volatilidade')
    axs[2].set_xlabel('Data')
    axs[2].legend()

    plt.tight_layout()
    plt.show()

# Chamando a função de plotagem
plot_data(df)

# Calculando correlações entre os retornos diários e a volatilidade
correlation_matrix = df[['Daily Returns', 'Volatility']].corr()
print("Matriz de Correlação:\n", correlation_matrix)

# Análise de desempenho do investimento
initial_investment = 10000  # Investimento inicial de $10,000
df['Investment Value'] = initial_investment * (1 + df['Daily Returns']).cumprod()

# Plotando o valor do investimento ao longo do tempo
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Investment Value'], label='Valor do Investimento', color='purple')
plt.title('Desempenho do Investimento ao Longo do Tempo')
plt.ylabel('Valor do Investimento ($)')
plt.xlabel('Data')
plt.legend()
plt.show()

# Exibindo os últimos 5 registros do dataframe
print(df.tail())
