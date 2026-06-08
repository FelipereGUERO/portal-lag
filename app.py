import streamlit as st
import pandas as pd
st.set_page_config(
   page_title="Portal LAG",
   page_icon="📊",
   layout="wide"
)
df = pd.read_csv("portal_links.csv")
df["ativo"] = df["ativo"].astype(str)
df = df[df["ativo"].str.lower().isin(["sim", "true", "1", "ativo"])]
st.title("📊 Portal LAG")
st.caption("Central de Dashboards e Ferramentas")
col1, col2, col3 = st.columns(3)
col1.metric("🏢 Áreas", df["area"].nunique())
col2.metric("🔗 Links", len(df))
col3.metric("📊 Power BIs", len(df[df["tipo"] == "Power BI"]))
st.divider()
busca = st.text_input(
   "🔍 Buscar dashboard, arquivo ou sistema"
)
if busca:
   resultado = df[
       df["nome"].str.contains(
           busca,
           case=False,
           na=False
       )
   ]
   st.subheader("Resultados")
   for _, row in resultado.iterrows():
       st.link_button(
           f"{row['nome']} | {row['area']}",
           row["link"],
           use_container_width=True
       )
else:
   areas = sorted(df["area"].unique())
   for area in areas:
       with st.expander(area):
           area_df = df[df["area"] == area]
           for _, row in area_df.iterrows():
               st.link_button(
                   f"{row['nome']} ({row['tipo']})",
                   row["link"],
                   use_container_width=True
               )
