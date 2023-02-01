import pandas as pd
import plotly.express as px
import streamlit as st

# Lendo as bases de dados

df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

df = pd.merge(df_vendas,df_produtos, how="left", on="ID Produto")


# CRIANDO COLUNAS NOVAS

# Qual o custo total?
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]

#Agora que temos a receita e custo total, podemos achar o Lucro total
#Vamos criar uma coluna de Lucro que será Receita - Custo
df["Lucro"] = df["Valor Venda"] - df["Custo"]

#criando uma coluna mes_ano
df["mes_ano"] = df["Data Venda"].dt.to_period("M").astype(str)


# AGRUPAMENTOS
produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()

lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()

lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()


#DataApp

def main():
    st.title("Análise de Vendas")
    st.image("vendas.png")

# Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Custo", df["Custo"].sum())
    col2.metric("Total Lucro", df["Lucro"].sum())
    col3.metric("Total Clientes", df["ID Cliente"].nunique())

# Gráficos
    col1, col2 = st.columns(2)

    fig1 = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', text="Quantidade", orientation="h", 
             title="Total Produtos vendidos por marca", width=380, height = 400)
    col1.plotly_chart(fig1)

    fig2 = px.pie(lucro_categoria, values='Lucro', names='Categoria', title='Lucro por categoria', width=380, height = 400)
    col2.plotly_chart(fig2)

    fig3 = px.line(lucro_mes_categoria, x='mes_ano', y='Lucro', markers=True, color="Categoria",
             title="LucroxMêsxCategoria")

    st.plotly_chart(fig3)

if __name__ == '__main__':
    main()