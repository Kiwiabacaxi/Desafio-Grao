import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_data():
    df = pd.read_csv("./data/commerce_dataset_clean.csv", sep=";", decimal=".")
    return df


# Calculando as métricas solicitadas


# 1 - Total de vendas no período
def total_sales(df):
    return df["total"].sum()


# 2 - Número total de produtos vendidos
def total_products_sold(df):
    return df["quantity"].sum()


# 3 - Média de preço unitário de linha de produtos
def average_unit_price(df):
    return df.groupby("product_line")["unit_price"].mean()

# 3 - Grafico de barras da média de preço unitário de linha de produtos
def plot_average_unit_price(df):
    # Calcular a média do preço unitário
    average_unit_price = df.groupby("product_line")["unit_price"].mean()

    # Criando um gráfico de barras personalizado com SEABORN
    plt.figure(figsize=(10, 8))
    barplot = sns.barplot(
        x=average_unit_price.index,
        y=average_unit_price.values,
        hue=average_unit_price.index,
        palette="viridis",
    )

    # Adicionando o valor de cada barra no topo
    for p in barplot.patches:
        barplot.annotate(
            format(p.get_height(), ".2f"),
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 9),
            textcoords="offset points",
        )

    plt.title("Média de Preço Unitário por Linha de Produto")
    plt.xlabel("Linha de Produto")
    plt.ylabel("Preço Unitário Médio")
    plt.xticks(rotation=45)

    # Deixar o eixo y a partir de 50
    # plt.ylim(50, None)

    plt.show()


# 4 - Linha de produto mais vendido (em termos de quantidade)
def most_sold_product_line(df):
    return df.groupby("product_line")["quantity"].sum().idxmax()


# 5 - As 5 linhas de produtos mais bem avaliados (média de rating mais alta)
def top_5_rated_product_lines(df):
    return df.groupby("product_line")["rating"].mean().nlargest(5)


# 6 - Loja com o maior volume de vendas
def store_with_highest_sales(df):
    return df.groupby("branch")["total"].sum().idxmax()


# Preparando para calcular o método de pagamento mais popular por loja e mês
def popular_payment_method_by_store_month(df):
    return (
        df.groupby(["branch", "month", "payment_method"])["invoice_id"]
        .count()
        .unstack()
        .idxmax(axis=1)
    )


# As 3 linhas de produtos com mais quantidades vendidas por gênero do cliente
def top_3_by_gender(df):
    return (
        df.groupby(["gender", "product_line"])["quantity"]
        .sum()
        .groupby(level=0, group_keys=False)
        .nlargest(3)
    )


# Produto mais lucrativo (maior receita gross_income) por filial (branch)
def most_profitable_by_branch(df):
    return (
        df.groupby(["branch", "product_line"])["gross_income"]
        .sum()
        .groupby(level=0, group_keys=False)
        .nlargest(1)
    )


# Produto mais lucrativo (maior receita gross_income) por quarter
def most_profitable_by_quarter(df):
    return (
        df.groupby(["quarter", "product_line"])["gross_income"]
        .sum()
        .groupby(level=0, group_keys=False)
        .nlargest(1)
    )


# Período do dia em que ocorre o maior número de vendas
def period_with_most_sales(df):
    return df["time_of_day"].value_counts().idxmax()
