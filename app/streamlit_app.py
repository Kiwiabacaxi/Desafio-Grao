import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# import seaborn as sns
# import matplotlib.pyplot as plt
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
    # st.write(pagamento_popular_por_loja_mes)
    # Preparar os dados
    pagamento_popular_por_loja_mes = popular_payment_method_by_store_month(df)
    pagamento_popular_por_loja_mes = pagamento_popular_por_loja_mes.reset_index()
    pagamento_popular_por_loja_mes = pagamento_popular_por_loja_mes.melt(
        id_vars=["branch", "month"], var_name="payment_method", value_name="value"
    )

    # Criar uma nova coluna combinando 'branch' e 'month'
    pagamento_popular_por_loja_mes["branch_month"] = (
        pagamento_popular_por_loja_mes["branch"]
        + " "
        + pagamento_popular_por_loja_mes["month"].astype(str)
    )

    # Multiplicar a coluna 'value' por 100
    pagamento_popular_por_loja_mes["value"] = (
        pagamento_popular_por_loja_mes["value"] * 100
    )

    # Criar o gráfico de barras empilhadas
    fig = px.bar(
        pagamento_popular_por_loja_mes,
        x="branch_month",
        y="value",
        color="payment_method",
        text="value",  # Adicionando o valor no topo das barras
        barmode="stack",
        labels={
            "branch_month": "Loja e Mês",
            "value": "Proporção (%)",
            "payment_method": "Método de Pagamento",
        },
        color_discrete_map={
            "Ewallet": "#54BEBE",
            "Credit card": "#dedad2",
            "Cash": "#c80064",
        },
    )

    # Personalizar o texto das barras
    fig.update_traces(
        texttemplate="%{text:.2f}%",  # Formatar o texto para mostrar duas casas decimais
        textposition="inside",
        textfont_size=12,
        # textfont_color="white",
    )

    # Personalizar o layout do gráfico
    fig.update_layout(
        xaxis_title="Loja e Mês",
        yaxis_title="Proporção (%)",
        title="Método de Pagamento Mais Popular por Loja e Mês",
        title_font=dict(size=30),
        xaxis_tickangle=-45,
        autosize=False,
        height=800,
        showlegend=True,
    )

    # Exibir o gráfico
    st.plotly_chart(fig, use_container_width=True)


elif option == "Top 3 Linhas de Produtos Mais Vendidos por Gênero":
    # st.write(top_3_por_genero)
    # Separando os dados por gênero
    male_data = top_3_por_genero[top_3_por_genero["gender"] == "Male"]
    female_data = top_3_por_genero[top_3_por_genero["gender"] == "Female"]

    # Definindo as cores padrão para todas as barras
    male_colors = [
        "lightslategray",
    ] * len(male_data)
    female_colors = [
        "lightslategray",
    ] * len(female_data)

    # Alterando a cor das barras para 'crimson' se 'is_top_3' for True
    male_colors = [
        "crimson" if is_top_3 else color
        for color, is_top_3 in zip(male_colors, male_data["is_top_3"])
    ]
    female_colors = [
        "crimson" if is_top_3 else color
        for color, is_top_3 in zip(female_colors, female_data["is_top_3"])
    ]

    # Criando as séries de barras
    male_bars = go.Bar(
        name="Male",
        x=male_data["product_line"],
        y=male_data["quantity"],
        marker_color=male_colors,
    )

    female_bars = go.Bar(
        name="Female",
        x=female_data["product_line"],
        y=female_data["quantity"],
        marker_color=female_colors,
    )

    # Criando o gráfico de barras
    fig = go.Figure(data=[male_bars, female_bars])

    # Atualizando o layout para empilhar as barras lado a lado
    fig.update_layout(
        barmode="group",
        title_text="Top 3 Linhas de Produtos Mais Vendidos por Gênero",
        xaxis_title="Linha de Produto",
        yaxis_title="Quantidade Vendida",
        title_font=dict(size=30),
        xaxis_tickangle=-45,
        autosize=False,
        height=800,
        showlegend=True, # as vezes fica melhor sem a legenda, testar
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif option == "Produto Mais Lucrativo por Filial":
    st.write(lucrativo_por_filial)

elif option == "Produto Mais Lucrativo por Quarter":
    st.write(lucrativo_por_quarter)

elif option == "Período do Dia com Mais Vendas":
    st.write(periodo_maior_vendas)
