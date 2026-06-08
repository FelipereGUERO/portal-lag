import streamlit as st
import pandas as pd
st.set_page_config(
   page_title="Portal LAG",
   layout="wide"
)
df = pd.read_csv("portal_links.csv")
df.columns = df.columns.str.strip().str.lower()
if "ativo" in df.columns:
   df = df[
       df["ativo"].astype(str).str.lower().isin(
           ["sim", "s", "true", "1", "ativo"]
       )
   ]
st.title("Portal LAG")
col1, col2, col3 = st.columns(3)
col1.metric("Areas", df["area"].nunique())
col2.metric("Links", len(df))
if "tipo" in df.columns:
   qtd_powerbi = len(
       df[
           df["tipo"].astype(str).str.contains(
               "power",
               case=False,
               na=False
           )
       ]
   )
else:
   qtd_powerbi = 0
col3.metric("Power BI", qtd_powerbi)
st.divider()
busca = st.text_input("Pesquisar")
if busca:
   resultado = df[
       df["nome"].astype(str).str.contains(
           busca,
           case=False,
           na=False
       )
   ]
   st.subheader("Resultados")
   for _, row in resultado.iterrows():
       st.link_button(
           f"{row['nome']} | {row['area']}",
           row["link"]
       )
else:
   areas = sorted(
       df["area"].dropna().unique()
   )
   for area in areas:
       with st.expander(area):
           area_df = df[
               df["area"] == area
           ]
           for _, row in area_df.iterrows():
               st.link_button(
                   row["nome"],
                   row["link"]
               )
