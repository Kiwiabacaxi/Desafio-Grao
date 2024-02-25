import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from logic.calc import (
    load_data,
    total_sales,
    total_products_sold,
    average_unit_price,
    most_sold_product_line,
    top_5_rated_product_lines,
    store_with_highest_sales,
    popular_payment_method_by_store_month,
    top_3_by_gender,
    most_profitable_by_branch,
    most_profitable_by_quarter,
    period_with_most_sales,
)

# Carregar o dataset
df = load_data()

# Calculando as métricas solicitadas
total_vendas = total_sales(df)
total_produtos_vendidos = total_products_sold(df)
media_preco_unitario = average_unit_price(df)
linha_mais_vendida = most_sold_product_line(df)
top_5_avaliados = top_5_rated_product_lines(df)
loja_maior_vendas = store_with_highest_sales(df)
pagamento_popular_por_loja_mes = popular_payment_method_by_store_month(df)
top_3_por_genero = top_3_by_gender(df)
lucrativo_por_filial = most_profitable_by_branch(df)
lucrativo_por_quarter = most_profitable_by_quarter(df)
periodo_maior_vendas = period_with_most_sales(df)

#############################################################

# Dashboard
# st.title("Dashboard de Desempenho de Vendas")

# Definindo as opções
options = [
    "Total de Vendas no Período",
    "Número Total de Produtos Vendidos",
    "Média de Preço Unitário",
    "Linha de Produto Mais Vendida",
    "Top 5 Linhas de Produtos Mais Bem Avaliados",
    "Loja com Maior Volume de Vendas",
    "Método de Pagamento Mais Popular por Loja e Mês",
    "Top 3 Linhas de Produtos Mais Vendidos por Gênero",
    "Produto Mais Lucrativo por Filial",
    "Produto Mais Lucrativo por Quarter",
    "Período do Dia com Mais Vendas",
]

# Adicionando um painel lateral
option = st.sidebar.selectbox(
    "Escolha a métrica que deseja visualizar",
    options,
)

# Exibindo apenas o contêiner correspondente à opção selecionada
if option == "Total de Vendas no Período":
    st.metric(label="Total de Vendas no Período", value=f"R$ {total_vendas:,.2f}")

elif option == "Número Total de Produtos Vendidos":
    st.metric(
        label="Número Total de Produtos Vendidos", value=f"{total_produtos_vendidos}"
    )

elif option == "Média de Preço Unitário":
    # Criando um gráfico de barras personalizado com Plotly
    fig = px.bar(
        media_preco_unitario,
        x=media_preco_unitario.index,
        # y="unit_price",
        y=media_preco_unitario.values,
        color=media_preco_unitario.index,
        # color_discrete_sequence=px.colors.qualitative.Plotly,
        template="xgridoff",
        labels={"UnitPrice": "Média de Preço Unitário", "Product": "Linha de Produto"},
    )

    # Personalizando o layout do gráfico
    fig.update_layout(
        xaxis_title="Linha de Produto",
        yaxis_title="Preço Unitário Médio",
        title="Média de Preço Unitário por Linha de Produto",
        title_font=dict(size=26),
        xaxis_tickangle=-45,
        yaxis=dict(range=[50, 60]),  # Definindo o limite inferior do eixo y para 50
        autosize=False,
        height=800,
    )

    # Exibindo o gráfico
    st.plotly_chart(fig, use_container_width=True)


elif option == "Linha de Produto Mais Vendida":
    st.write(linha_mais_vendida)

elif option == "Top 5 Linhas de Produtos Mais Bem Avaliados":
    st.write(top_5_avaliados)

elif option == "Loja com Maior Volume de Vendas":
    st.write(loja_maior_vendas)

elif option == "Método de Pagamento Mais Popular por Loja e Mês":
    st.write(pagamento_popular_por_loja_mes)

elif option == "Top 3 Linhas de Produtos Mais Vendidos por Gênero":
    st.write(top_3_por_genero)

elif option == "Produto Mais Lucrativo por Filial":
    st.write(lucrativo_por_filial)

elif option == "Produto Mais Lucrativo por Quarter":
    st.write(lucrativo_por_quarter)

elif option == "Período do Dia com Mais Vendas":
    st.write(periodo_maior_vendas)
