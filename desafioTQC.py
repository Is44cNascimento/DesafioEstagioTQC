import pandas as pandas
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="INSIGHT DE CONTROLE DE VENDAS E PAGAMENTOS",
    layout="wide",
    initial_sidebar_state="expanded", )



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
st.dataframe(ControleVendasPagamentos_filtro, height=600, width=900)

tabelaCor = ControleVendasPagamentos.groupby('Cor').agg({'Quantidade':'sum'}).reset_index()
print(tabelaCor.head())

tabelaTamanho = ControleVendasPagamentos.groupby('Tamanho').agg({ 'Quantidade':'sum'}).reset_index()

print(tabelaTamanho.head())

totalValorPago = ControleVendasPagamentos['ValorPago'].sum()
totalValorPendente = ControleVendasPagamentos['Valor Pendente'].sum()

st.metric(label="Total De Valor Pago", value=f"R$ {totalValorPago:.2f}")
st.metric(label="Total De Valor PEndente", value=f"R$ {totalValorPendente:.2f}")

tabelaValorPago = ControleVendasPagamentos.groupby('Cliente').agg({'ValorPago': 'sum'}).reset_index()
tabelaValorPendente = ControleVendasPagamentos.groupby('Cliente').agg({'Valor Pendente': 'sum'}).reset_index()

st.subheader("Grafico de valor pago ou pendente")

graficoValorPago = px.bar(
    tabelaValorPago,
    x='Cliente',
    y='ValorPago',
    labels={'Clientes': 'Clientes','ValorPago': 'ValorPago (R$)' },
    title='Grafico de valor pago por cliente',
    text_auto= True
)

graficoValorPendente = px.bar(
    tabelaValorPendente,
    x='Cliente',
    y='Valor Pendente',
    labels={'Clientes': 'Clientes','Valor Pendente': 'Valor Pendente (R$)' },
    title='Grafico de valor pendente por cliente',
    text_auto= True
)


st.plotly_chart(graficoValorPago)
st.plotly_chart(graficoValorPendente)

st.sidebar.subheader("SELECIONAR O TIPO DE GRAFICO PARA TAMANHO")
tipoGrafico = st.sidebar.selectbox(
    "SELECIONAR O TIPO DE GRAFICO PARA `QUANTIDADE POR TAMANHO`:",
    options=['GRAFICO DE BARRAS' , 'GRAFICO DE PIZZA'],key='POR TAMANHO')

if tipoGrafico == 'GRAFICO DE PIZZA':
    TabelaTamanhoGrafico = px.pie(
        tabelaTamanho,
        names='Tamanho',
        values='Quantidade',
        labels={'Tamanho': 'Tamanho' },
        title='QUANTIDADE POR TAMANHO NO GRAFICO DE PIZZA'
)
elif tipoGrafico == 'GRAFICO DE BARRAS':
    TabelaTamanhoGrafico = px.bar(
        tabelaTamanho,
        x='Tamanho',
        y='Quantidade',
        labels={'Tamanho': 'Tamanho', 'Quantidade': 'Quantidade' },
        title='QUANTIDADE POR TAMANHO NO GRAFICO DE PIZZA'
    )

st.plotly_chart(TabelaTamanhoGrafico)


st.sidebar.subheader("SELECIONAR O TIPO DE GRAFICO")
tipoGrafico = st.sidebar.selectbox(
    "SELECIONAR O TIPO DE GRAFICO PARA `QUANTIDADE POR COR`:",
    options=['GRAFICO DE BARRAS' , 'GRAFICO DE PIZZA'],key='Por cor')

if tipoGrafico == 'GRAFICO DE BARRAS':
    TabelaCorGrafico = px.bar(
        tabelaCor,
        x='Cor',
        y='Quantidade',
        labels={'Cor': 'Cores', 'Quantidade': 'Quantidade de cor vendida'},
        title='QUANTIDADE POR CORES NO GRAFICO DE BARRAS'
)
elif tipoGrafico == 'GRAFICO DE PIZZA':
    TabelaCorGrafico = px.pie(
        tabelaCor,
        names='Cor',
        values='Quantidade',
        labels={'Cor': 'Cores', 'Quantidade': 'Quantidade de cor vendida'},
        title='QUANTIDADE POR CORES NO GRAFICO DE PIZZA'

    )


st.plotly_chart(TabelaCorGrafico)


