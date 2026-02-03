import pandas as pandas
import streamlit as st
import plotly.express as px



ControleVendasPagamentos  = pandas.read_excel('ControleVendasPagamentos.xlsx')


ControleVendasPagamentos.columns = ControleVendasPagamentos.columns.str.strip()



tabelaDinamicaQuantidade =  pandas.pivot_table(ControleVendasPagamentos,
                            values='Quantidade',
                            index=['Cliente'],
                            columns=['Produto'],
                            aggfunc='sum',
                            fill_value=0)

print(tabelaDinamicaQuantidade)


tabelaDinamicaCor =  pandas.pivot_table(ControleVendasPagamentos,
                            values='Quantidade',
                            index=['Cor'],
                            aggfunc='max')

print(tabelaDinamicaCor)

tabelaDinamicaTamanho =  pandas.pivot_table(ControleVendasPagamentos,
                            values='Quantidade',
                            index=['Tamanho'],
                            aggfunc='max')

print(tabelaDinamicaTamanho)

st.title("Insight de controle de vendas e pagamentos ")
st.sidebar.title("opcoes de filtro")


clientes = st.sidebar.multiselect(
    "Para selecionar os clientes",
    options= ControleVendasPagamentos['Cliente'].unique(),
    default= ControleVendasPagamentos['Cliente'].unique()
)

Produtos = st.sidebar.multiselect(
    "Para selecionar os produtos",
    options= ControleVendasPagamentos['Produto'].unique(),
    default= ControleVendasPagamentos['Produto'].unique()
)

ControleVendasPagamentos_filtro = ControleVendasPagamentos[(ControleVendasPagamentos['Cliente'].isin(clientes)) & (ControleVendasPagamentos['Produto'].isin(Produtos))]


st.subheader("Tabela filtrada")
st.dataframe(ControleVendasPagamentos_filtro)

tabelaCor = ControleVendasPagamentos.groupby('Cor').agg({'Quantidade':'sum'}).reset_index()
print(tabelaCor.head())

tabelaTamanho = ControleVendasPagamentos.groupby('Tamanho').agg({ 'Quantidade':'sum'}).reset_index()
st.subheader("Quantidade por cor")
print(tabelaTamanho.head())

tabelaCorGrafico = px.bar(
    tabelaCor,
    x='Cor',
    y='Quantidade',
    labels={'Cor': 'Cores', 'Quantidade': 'Quantidade de cor vendida'},
    title='Quantidade por cor'
)

TabelaTamanhoGrafico = px.pie(
    tabelaTamanho,
    names = 'Tamanho',
    values='Quantidade',
    labels={'Tamanho': 'Tamanho' },
    title='Quantidade por Tamanho'
)


st.plotly_chart(tabelaCorGrafico)
st.plotly_chart(TabelaTamanhoGrafico)


