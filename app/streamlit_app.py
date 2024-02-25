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
    colors_spring_pastels = [
        "#fd7f6f",
        "#7eb0d5",
        "#b2e061",
        "#bd7ebe",
        "#ffb55a",
        "#ffee65",
        "#beb9db",
        "#fdcce5",
        "#8bd3c7",
    ]

    colors_viridis_6 = [
        "#fde725",
        "#7ad151",
        "#22a884",
        "#2a788e",
        "#414487",
        "#440154",
    ]

    # Criando um gráfico de barras personalizado com Plotly
    fig = px.bar(
        media_preco_unitario,
        x=media_preco_unitario.index,
        y="unit_price",
        # y=media_preco_unitario.values,
        color=media_preco_unitario.index,
        # color_discrete_sequence=colors_spring_pastels,
        color_discrete_sequence=colors_viridis_6,
        labels={"UnitPrice": "Média de Preço Unitário", "Product": "Linha de Produto"},
    )

    # Personalizando o layout do gráfico
    fig.update_layout(
        xaxis_title="Linha de Produto",
        yaxis_title="Preço Unitário Médio",
        title="Média de Preço Unitário por Linha de Produto",
        title_font=dict(size=32),
        xaxis_tickangle=-45,
        yaxis=dict(range=[50, 60]),  # Definindo o limite inferior do eixo y para 50
        height=800,
        showlegend=False,
    )

    # Exibindo o gráfico
    st.plotly_chart(fig, use_container_width=True)


elif option == "Linha de Produto Mais Vendida":
    # st.write(linha_mais_vendida)

    # color low hue RED
    color_deemphasized = [
        "#F0CBC5",
        "#EA5543",  # Cor Forte
    ]

    # Criando um gráfico de barras com Plotly
    fig = px.bar(
        linha_mais_vendida,
        x="product_line",
        y="quantity",
        color="is_most_sold",
        labels={"product_line": "Linha de Produto", "quantity": "Quantidade Vendida"},
        color_discrete_map={False: color_deemphasized[0], True: color_deemphasized[1]},
    )

    # Personalizando o layout do gráfico
    fig.update_layout(
        xaxis_title="Linha de Produto",
        yaxis_title="Quantidade Vendida",
        title="Linha de Produto Mais Vendida",
        title_font=dict(size=32),
        xaxis_tickangle=-45,
        autosize=False,
        yaxis=dict(range=[800, 1000]),  # Definindo o limite inferior do eixo y para 800
        height=800,
        showlegend=False,  # Escondendo a legenda
    )

    # Exibindo o gráfico
    st.plotly_chart(fig, use_container_width=True)

elif option == "Top 5 Linhas de Produtos Mais Bem Avaliados":
    # Definindo as cores
    color_deemphasized = [
        "#F0CBC5",
        "#EA5543",  # Cor Forte
    ]

    # Criando um gráfico de barras com Plotly
    fig = px.bar(
        top_5_avaliados,
        x="product_line",
        y="rating",
        color="is_top5",
        labels={"product_line": "Linha de Produto", "rating": "Avaliação Média"},
        color_discrete_map={False: color_deemphasized[0], True: color_deemphasized[1]},
    )

    # Personalizando o layout do gráfico
    fig.update_layout(
        xaxis_title="Linha de Produto",
        yaxis_title="Avaliação Média",
        title="Top 5 Linhas de Produtos Mais Bem Avaliados",
        title_font=dict(size=32),
        xaxis_tickangle=-45,
        autosize=False,
        height=800,
        yaxis=dict(range=[6, 7.4]),  # Definindo o limite inferior do eixo y
        showlegend=False,  # Escondendo a legenda
    )

    # Exibindo o gráfico
    st.plotly_chart(fig, use_container_width=True)

elif option == "Loja com Maior Volume de Vendas":
    # st.write(type(loja_maior_vendas))
    # Definindo as cores
    color_deemphasized = [
        "#F0CBC5",
        "#EA5543",  # Cor Forte
    ]

    # Criando um gráfico de barras com Plotly
    fig = px.bar(
        loja_maior_vendas,
        x="branch",
        y="total",
        color="is_top",
        labels={"branch": "Loja", "total": "Volume de Vendas"},
        color_discrete_map={False: color_deemphasized[0], True: color_deemphasized[1]},
    )

    # Personalizando o layout do gráfico
    fig.update_layout(
        xaxis_title="Loja",
        yaxis_title="Volume de Vendas",
        title="Loja com Maior Volume de Vendas",
        title_font=dict(size=32),
        xaxis_tickangle=-45,
        autosize=False,
        height=800,
        yaxis=dict(
            range=[100_000, 112_000]  # 106_000 altera bastante a percepção
        ),  # Definindo o limite inferior do eixo y
        showlegend=False,  # Escondendo a legenda
    )

    # Exibindo o gráfico
    st.plotly_chart(fig, use_container_width=True)

elif option == "Método de Pagamento Mais Popular por Loja e Mês":
    st.write((pagamento_popular_por_loja_mes))
    # popular_payment_method = pagamento_popular_por_loja_mes

    # # Criando um gráfico de barras empilhadas com Plotly
    # fig = px.bar(
    #     popular_payment_method.reset_index(),
    #     x="branch",
    #     y=popular_payment_method.columns.tolist(),
    #     labels={"value": "Proporção", "branch": "Loja", "variable": "Método de Pagamento"},
    #     title="Método de Pagamento Mais Popular por Loja e Mês",
    #     height=800,
    # )

    # # Personalizando o layout do gráfico
    # fig.update_layout(
    #     barmode="stack",
    #     xaxis={"categoryorder": "total descending"},
    #     yaxis_title="Proporção",
    # )

    # # Exibindo o gráfico
    # st.plotly_chart(fig, use_container_width=True)


elif option == "Top 3 Linhas de Produtos Mais Vendidos por Gênero":
    st.write(top_3_por_genero)

elif option == "Produto Mais Lucrativo por Filial":
    st.write(lucrativo_por_filial)

elif option == "Produto Mais Lucrativo por Quarter":
    st.write(lucrativo_por_quarter)

elif option == "Período do Dia com Mais Vendas":
    st.write(periodo_maior_vendas)
