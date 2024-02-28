import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image


from streamlit_option_menu import option_menu

from logic.calc import (
    load_data,
    overview,
    describe,
    data_types,
    duplicated_values,
    missing_values,
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
    sales_by_quarter_city_category,
)

from logic.pred_calc import load_data_pred, prepare_data, train_sarima, make_forecast

# Carregar o dataset
df = load_data()

# Visão geral do dataset
visao_geral = overview(df)
descrever = describe(df)
tipos_dados = data_types(df)
valores_duplicados = duplicated_values(df)
valores_nulos = missing_values(df)

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
vendas_por_quarter_cidade_categoria = sales_by_quarter_city_category(df)


# # Carregar os dados para previsão - SARIMA
# df_pred = load_data_pred()
# train_data, test_data = prepare_data(df_pred)
# model_sarima_fit = train_sarima(train_data, p=1, d=1, q=1, P=1, D=1, Q=1, m=7)
# forecast_mean, forecast_ci = make_forecast(model_sarima_fit, test_data)


#############################################################

# Dashboard
im = Image.open("app/img/favicon.ico")
st.set_page_config(
    page_title="Dashboard",
    page_icon=im,
    layout="wide",
)

# Definindo as opções
options = [
    "Visão Geral do Dataset",
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
    "Análise de Vendas por Trimestre, Região e Categoria",
    "Modelo de Previsão de Vendas - SARIMA",
]

with st.sidebar:
    st.title("Dashboard")
    option = option_menu(
        # menu_title="Escolha a métrica que deseja visualizar",
        # menu_title="Menu",
        menu_title="Metricas",
        menu_icon="cast",
        options=options,
        default_index=0,
        styles={
            "container": {
                # "padding": "0!important",
                "background-color": "#393e48"
            },
            "icon": {"color": "#f1f1f1", "font-size": "14px"},
            "nav-link": {
                # "font-size": "25px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#505764",
            },
            "nav-link-selected": {
                "background-color": "#ff2e63",
            },
        },
    )


if option == "Visão Geral do Dataset":
    # Exibindo a visão geral do datase
    st.subheader("Visão Geral do Dataset")
    st.dataframe(visao_geral)

    # Exibindo informações adicionais
    st.subheader("Informações Adicionais")
    st.table(descrever)

    # Exibindo os tipos de dados
    tipos_dados.columns = ["Nome da Coluna", "Tipo de Dado"]
    st.subheader("Tipos de Dados")
    st.table(tipos_dados)

    # Exibindo valores nulos
    st.subheader("Valores Nulos")
    st.table(valores_nulos)

    # Exibindo valores duplicados
    st.subheader("Valores Duplicados")
    st.write(f"Total de Valores Duplicados: {valores_duplicados}")

elif option == "Total de Vendas no Período":
    st.markdown(
        f"""
    <div style="display: flex; flex-direction: column; text-align: center;">
        <h2 style="font-size: 32px; font-weight: bold;">Total de Vendas no Período</h2>
        <h1 style="font-size: 48px;">R$ {total_vendas:,.2f}</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

elif option == "Número Total de Produtos Vendidos":
    st.markdown(
        f"""
    <div style="display: flex; flex-direction: column; text-align: center;">
        <h2 style="font-size: 32px; font-weight: bold;">Número Total de Produtos Vendidos</h2>
        <h1 style="font-size: 48px;">{total_produtos_vendidos}</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

elif option == "Média de Preço Unitário":
    color_pink_foam_7 = [
        "#54bebe",
        "#90cfcf",
        "#c2e0df",
        "#f1f1f1",
        "#ebb0bf",
        "#dd6e90",
        "#c80064",
    ]

    # Criando um gráfico de barras personalizado com Plotly
    fig = px.bar(
        media_preco_unitario,
        x=media_preco_unitario.index,
        y="unit_price",
        # y=media_preco_unitario.values,
        color=media_preco_unitario.index,
        color_discrete_sequence=color_pink_foam_7,
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
        "#FF2E63",  # Cor Forte v3 - crimson_v3
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
        "#FF2E63",  # Cor Forte v3 - crimson_v3
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
        autosize=True,
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
        "#FF2E63",  # Cor Forte v3 - crimson_v3
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
            "Ewallet": "#54bebe",
            "Credit card": "#f1f1f1",
            "Cash": "#ff2e63",
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
        title_font=dict(size=32),
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
        "#F0CBC5",
    ] * len(male_data)
    female_colors = [
        "#F0CBC5",
    ] * len(female_data)

    # Alterando a cor das barras para '#FF2E63' se 'is_top_3' for True
    male_colors = [
        "#FF2E63" if is_top_3 else color
        for color, is_top_3 in zip(male_colors, male_data["is_top_3"])
    ]
    female_colors = [
        "#FF2E63" if is_top_3 else color
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
        title_font=dict(size=32),
        xaxis_tickangle=-45,
        autosize=False,
        yaxis=dict(range=[300, 600]),  # Definindo o limite inferior do eixo y
        height=800,
        showlegend=False,
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif option == "Produto Mais Lucrativo por Filial":
    # st.write(lucrativo_por_filial)
    # Definindo a escala de cores
    colors = [
        "#54bebe",
        "#f1f1f1",
        "#ff2e63",
    ]
    # Obtendo os dados mais lucrativos por filial
    lucrativo_por_filial = most_profitable_by_branch(df)

    # Convertendo o índice multi-nível em colunas
    lucrativo_por_filial = lucrativo_por_filial.reset_index()

    # Criando o gráfico de barras
    fig = go.Figure()

    # Criando uma série de dados para cada filial
    for branch, color in zip(lucrativo_por_filial["branch"].unique(), colors):
        branch_data = lucrativo_por_filial[lucrativo_por_filial["branch"] == branch]
        fig.add_trace(
            go.Bar(
                name=branch,
                x=branch_data["product_line"],
                y=branch_data["gross_income"],
                marker_color=color,
            )
        )

    # Atualizando o layout do gráfico
    fig.update_layout(
        title_text="Produto Mais Lucrativo por Filial",
        xaxis_title="Filial",
        yaxis_title="Lucro",
        title_font=dict(size=32),
        xaxis_tickangle=-45,
        autosize=False,
        yaxis=dict(range=[800, 1200]),  # Definindo o limite inferior do eixo y
        height=800,
        showlegend=True,
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif option == "Produto Mais Lucrativo por Quarter":
    # st.write(lucrativo_por_quarter)
    # Obtendo os dados mais lucrativos por quarter
    lucrativo_por_quarter = most_profitable_by_quarter(df)

    # Cores
    color_pink_foam_palette_divergent_6 = [
        "#54bebe",
        "#90cfcf",
        "#c2e0df",
        "#f1f1f1",
        "#ff9ea7",
        "#ff2e63",
    ]

    # Ordenando o DataFrame por gross_income
    lucrativo_por_quarter = lucrativo_por_quarter.sort_values(by="gross_income")

    # Mapeando as cores para os produtos em ordem
    color_mapping = dict(
        zip(lucrativo_por_quarter["product_line"], color_pink_foam_palette_divergent_6)
    )

    # Criando o gráfico de rosquinha
    fig = go.Figure(
        data=[
            go.Pie(
                labels=lucrativo_por_quarter["product_line"],
                values=lucrativo_por_quarter["gross_income"],
                hole=0.45,
                pull=[
                    0.2 if i == "Most Profitable" else 0
                    for i in lucrativo_por_quarter["most_profitable"]
                ],
                marker=dict(
                    colors=[
                        color_mapping[product]
                        for product in lucrativo_por_quarter["product_line"]
                    ]
                ),  # Use a paleta de cores personalizada
            )
        ]
    )  # hole parameter creates the donut shape

    # Atualizando o layout do gráfico
    fig.update_layout(
        title_text="Produto Mais Lucrativo por Quarter",
        title_font=dict(size=32),
        autosize=False,
        height=800,
        showlegend=True,
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif option == "Período do Dia com Mais Vendas":
    # st.write(periodo_maior_vendas)
    # Obtendo o número de vendas por período do dia
    sales_by_time_period = period_with_most_sales(df)

    # Mapeando as cores para os períodos do dia
    # color_mapping = {"morning": "blue", "afternoon": "green", "evening": "red"}
    color_mapping = {
        "morning": "#54bebe",
        # "morning": "#a9d8d7", # pastel color
        "afternoon": "#f1f1f1",
        # "evening": "#e590a7", # pastel color
        "evening": "#ff2e63",
    }

    # Criando o gráfico de barras
    fig = go.Figure(
        data=[
            go.Bar(
                x=sales_by_time_period["time_of_day"],
                y=sales_by_time_period["sales_count"],
                marker_color=[
                    color_mapping[time] for time in sales_by_time_period["time_of_day"]
                ],
            )
        ]
    )

    # Atualizando o layout do gráfico
    fig.update_layout(
        title_text="Número de Vendas por Período do Dia",
        xaxis_title="Período do Dia",
        yaxis_title="Número de Vendas",
        autosize=False,
        height=800,
        showlegend=False,
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif option == "Análise de Vendas por Trimestre, Região e Categoria":
    # Cores padrão do projeto
    color_pink_foam_palette_divergent = [
        "#54bebe",
        "#f1f1f1",
        "#ff2e63",
    ]

    # Invertendo a lista de cores
    color_pink_foam_palette_divergent_r = color_pink_foam_palette_divergent[::-1]

    # Criação do gráfico de treemap
    fig = px.treemap(
        vendas_por_quarter_cidade_categoria,
        path=["quarter", "city", "product_line"],
        values="total",
        color="total",
        color_continuous_scale=color_pink_foam_palette_divergent,
        # color_discrete_sequence=color_pink_foam_palette_divergent,
    )

    # Atualizando o layout do gráfico
    fig.update_traces(
        root_color="lightgrey",  # Adicionando cor de fundo
        marker=dict(cornerradius=5),  # Adicionando bordas arredondadas
        # hoverinfo="label",  # Adicionando informações ao passar o mouse
    )

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # Atualizando o layout do gráfico
    fig.update_layout(
        title_text="Tree Map - Análise de Vendas por Trimestre, Cidade e Categoria",
        title_font=dict(size=32),
        autosize=False,
        height=800,
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif option == "Modelo de Previsão de Vendas - SARIMA":
    # Carregar os dados para previsão - SARIMA
    df_pred = load_data_pred()

    # Adicionar slider para o parâmetro split_ratio
    st.header("Parâmetro de divisão dos dados")
    split_ratio = st.slider(
        "Proporção de divisão dos dados (treinamento / teste)",
        min_value=0.1,
        max_value=0.9,
        value=0.2,
        step=0.1,
    )
    st.markdown(
        "split_ratio: A proporção dos dados que será usada para treinamento. O restante será usado para teste."
    )

    # Preparar os dados com a proporção de divisão selecionada
    train_data, test_data = prepare_data(df_pred, split_ratio)

    # Adicionar sliders para os parâmetros do modelo SARIMA
    st.header("Parâmetros do Modelo SARIMA")

    with st.expander("Componentes não sazonais"):
        col1, col2, col3 = st.columns(3)
        with col1:
            p = st.slider(
                "Ordem do componente autoregressivo (p)",
                min_value=0,
                max_value=5,
                value=1,
            )
            st.markdown("p: A ordem do componente autoregressivo do modelo.")
        with col2:
            d = st.slider(
                "Grau de diferenciação (d)", min_value=0, max_value=5, value=1
            )
            st.markdown("d: O grau de diferenciação envolvido.")
        with col3:
            q = st.slider(
                "Ordem do componente de média móvel (q)",
                min_value=0,
                max_value=5,
                value=1,
            )
            st.markdown("q: A ordem do componente de média móvel do modelo.")

    with st.expander("Componentes sazonais"):
        col1, col2, col3 = st.columns(3)
        with col1:
            P = st.slider(
                "Ordem do componente autoregressivo sazonal (P)",
                min_value=0,
                max_value=5,
                value=1,
            )
            st.markdown("P: A ordem do componente autoregressivo sazonal do modelo.")
        with col2:
            D = st.slider(
                "Grau de diferenciação sazonal (D)", min_value=0, max_value=5, value=1
            )
            st.markdown(
                "D: O grau de diferenciação envolvido na parte sazonal do modelo."
            )
        with col3:
            Q = st.slider(
                "Ordem do componente de média móvel sazonal (Q)",
                min_value=0,
                max_value=5,
                value=1,
            )
            st.markdown("Q: A ordem do componente de média móvel sazonal do modelo.")
            m = st.slider(
                "Número de etapas de tempo para um único período sazonal (m)",
                min_value=2,
                max_value=12,
                value=7,
            )
            st.markdown("m: O número de etapas de tempo para um único período sazonal.")

    # Treinar o modelo SARIMA com os parâmetros selecionados
    model_sarima_fit = train_sarima(train_data, p=p, d=d, q=q, P=P, D=D, Q=Q, m=m)

    # Fazer a previsão
    forecast_mean, forecast_ci = make_forecast(model_sarima_fit, test_data)

    # Cores padrão do projeto
    color_pink_foam_palette_divergent = [
        "#54bebe",
        "#f1f1f1",
        "#ff2e63",
    ]

    # Cria um objeto de figura
    fig = go.Figure()

    # Adiciona os dados de treinamento ao gráfico
    fig.add_trace(
        go.Scatter(
            x=train_data.index,
            y=train_data,
            mode="lines",
            name="Dados de Treinamento",
            line=dict(color=color_pink_foam_palette_divergent[0]),
        )
    )

    # Adiciona os dados de teste ao gráfico
    fig.add_trace(
        go.Scatter(
            x=test_data.index,
            y=test_data,
            mode="lines",
            name="Dados de Teste",
            line=dict(color=color_pink_foam_palette_divergent[1]),
        )
    )

    # Adiciona as previsões ao gráfico
    fig.add_trace(
        go.Scatter(
            x=forecast_mean.index,
            y=forecast_mean,
            mode="lines",
            name="Previsões",
            line=dict(color=color_pink_foam_palette_divergent[2]),
        )
    )

    # Adiciona o intervalo de confiança ao gráfico
    fig.add_trace(
        go.Scatter(
            x=forecast_ci.index,
            y=forecast_ci.iloc[:, 0],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_ci.index,
            y=forecast_ci.iloc[:, 1],
            mode="lines",
            fill="tonexty",
            line=dict(width=0),
            # fillcolor="rgba(255, 0, 0, 0.3)",
            fillcolor="rgba(255, 46, 99, 0.3)",
            showlegend=False,
        )
    )

    # Adiciona títulos e rótulos
    fig.update_layout(
        title="Previsão de Vendas Futuras com Modelo SARIMA",
        title_font=dict(size=32),
        xaxis_title="Data",
        yaxis_title="Total de Vendas",
        height=800,
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
