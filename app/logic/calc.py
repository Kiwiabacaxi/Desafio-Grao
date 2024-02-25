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


# 4 - Linha de produto mais vendido (em termos de quantidade)
# def most_sold_product_line(df):
#     return df.groupby("product_line")["quantity"].sum().idxmax()
def most_sold_product_line(df):
    # Calcule a quantidade vendida por linha de produto
    quantity_per_product_line = (
        df.groupby("product_line")["quantity"].sum().reset_index()
    )

    # Encontre a linha de produto mais vendida
    most_sold_product = quantity_per_product_line.loc[
        quantity_per_product_line["quantity"].idxmax(), "product_line"
    ]

    # Crie uma nova coluna que é True para a linha de produto mais vendida e False para as outras
    quantity_per_product_line["is_most_sold"] = (
        quantity_per_product_line["product_line"] == most_sold_product
    )

    return quantity_per_product_line


# 5 - As 5 linhas de produtos mais bem avaliados (média de rating mais alta)
# def top_5_rated_product_lines(df):
#     return df.groupby("product_line")["rating"].mean().nlargest(5)
def top_5_rated_product_lines(df):
    # Calcule a média de rating para cada linha de produto
    average_rating = df.groupby("product_line")["rating"].mean().reset_index()

    # Selecione as 5 linhas de produtos com a média de rating mais alta
    top5_product_lines = average_rating.nlargest(5, "rating").index

    # Crie uma nova coluna que é True para as top 5 linhas de produtos e False para as outras
    average_rating["is_top5"] = average_rating.index.isin(top5_product_lines)

    return average_rating


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
