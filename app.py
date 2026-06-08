import streamlit as st
st.set_page_config(
   page_title="Portal LAG",
   page_icon="📊",
   layout="wide"
)
dados = {
   "📅 Planejamento": [
       ("📊 S&OP", "https://www.google.com"),
       ("📊 Forecast", "https://www.google.com")
   ],
   "🚚 Logística": [
       ("📊 Dashboard Estoque", "https://www.google.com"),
       ("📊 Torre de Controle", "https://www.google.com"),
       ("📊 Transportes", "https://www.google.com")
   ],
   "🌎 Comex": [
       ("📊 Importação", "https://www.google.com")
   ],
   "🛒 Compras": [
       ("📊 Spend Analysis", "https://www.google.com")
   ],
   "⚙️ Lean": [
       ("📊 Kaizens", "https://www.google.com")
   ],
   "✅ Qualidade": [
       ("📊 Indicadores Qualidade", "https://www.google.com")
   ],
   "💰 Pricing": [
       ("📊 Simulador de Preços", "https://www.google.com")
   ]
}
if "area" not in st.session_state:
   st.session_state.area = None
st.title("📊 Portal LAG")
if st.session_state.area is None:
   st.subheader("Áreas")
   for area in dados.keys():
       if st.button(area, use_container_width=True):
           st.session_state.area = area
           st.rerun()
else:
   area = st.session_state.area
   st.subheader(area)
   for nome, link in dados[area]:
       st.link_button(
           nome,
           link,
           use_container_width=True
       )
   if st.button("🔙 Voltar"):
       st.session_state.area = None
       st.rerun()
