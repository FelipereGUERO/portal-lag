import streamlit as st
import pandas as pd

st.set_page_config(
   page_title="Portal LAG",
   page_icon="📊",
   layout="wide"
)

# Ler CSV
df = pd.read_csv("portal_links.csv")

# Limpeza básica
df.columns = df.columns.str.strip().str.lower()

# Filtrar somente ativos (se existir a coluna)
if "ativo" in df.columns:
   df = df[df["ativo"].astype(str).str.lower().isin(
       ["sim", "s", "true", "1", "ativo"]
   )]

# Título
st.title("📊 Portal LAG")
st.caption("Central de Dashboards e Ferramentas")

# Métricas
col1, col2, col3 = st.columns(3)

col1.metric("🏢 Áreas", df["area"].nunique())
col2.metric("🔗 Links", len(df))
col3.metric(
   "📊 Power BIs",
   len(df[df["tipo"].astype(str).str.contains("power", case=False, na=False)])
)

st.divider()

# Busca
busca = st.text_input(
   "🔍 Buscar dashboard, arquivo ou sistema"
)

if busca:

   resultado = df[
       df["nome"].astype(str).str.contains(
           busca,
           case=False,
           na=False
       )
   ]

   st.subheader("Resultados")

   if len(resultado) == 0:
       st.warning("Nenhum resultado encontrado.")

   for _, row in resultado.iterrows():

       st.link_button(
           f"{row['nome']} | {row['area']}",
           row["link"],
           use_container_width=True
       )

else:

   areas = sorted(df["area"].dropna().unique())

   for area in areas:

       with st.expander(f"📂 {area}"):

           area_df = df[df["area"] == area]

           tipos = area_df["tipo"].dropna().unique()

           for tipo in tipos:

               st.markdown(f"### {tipo}")

               tipo_df = area_df[
                   area_df["tipo"] == tipo
               ]

               for _, row in tipo_df.iterrows():

                   st.link_button(
                       row["nome"],
                       row["link"],
                       use_container_width=True
                   )
