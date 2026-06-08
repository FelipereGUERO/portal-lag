
import streamlit as st

st.set_page_config(
   page_title="Portal LAG",
   page_icon="📊",
   layout="wide"
)

# DADOS DE TESTE
dados = {
   "Planejamento": [
       ("📊 S&OP", "https://google.com"),
       ("📊 Forecast", "https://google.com"),
   ],

   "Logística": [
       ("📊 Dashboard Estoque", "https://google.com"),
       ("📊 Torre de Controle", "https://google.com"),
       ("📊 Transportes", "https://google.com"),
   ],

   "Comex": [
       ("📊 Importação", "https://google.com"),
       ("📊 Exportação", "https://google.com"),
   ],

   "Compras": [
       ("📊 Spend Analysis", "https://google.com"),
   ],

   "Lean": [
       ("📊 Kaizens", "https://google.com"),
   ],

   "Qualidade": [
       ("📊 Indicadores Qualidade", "https://google.com"),
   ],

   "Pricing": [
       ("📊 Simulador de Preços", "https://google.com"),
   ]
}

st.title("📊 Portal LAG")

st.caption(
   "Central de Dashboards, Indicadores e Ferramentas"
)

busca = st.text_input(
   "🔍 Pesquisar dashboard"
)

st.divider()

for area, links in dados.items():

   with st.expander(area, expanded=False):

       for nome, url in links:

           if busca.lower() in nome.lower():

               st.link_button(
                   nome,
                   url,
                   use_container_width=True
               )

