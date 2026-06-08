import streamlit as st
st.set_page_config(
   page_title="Portal LAG",
   page_icon="📊",
   layout="wide"
)
dados = {
   "📅 Planejamento": 2,
   "🚚 Logística": 5,
   "🌎 Comex": 3,
   "🛒 Compras": 4,
   "⚙️ Lean": 2,
   "✅ Qualidade": 3,
   "💰 Pricing": 2
}
st.title("📊 Portal LAG")
st.caption("Central de Dashboards, Indicadores e Ferramentas")
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
   st.metric("🏢 Áreas", len(dados))
with col2:
   st.metric("📊 Dashboards", sum(dados.values()))
with col3:
   st.metric("👥 Usuários", "LAG")
st.divider()
st.subheader("📂 Áreas")
col1, col2, col3 = st.columns(3)
areas = list(dados.items())
for i, (area, qtd) in enumerate(areas):
   coluna = [col1, col2, col3][i % 3]
   with coluna:
st.info(f"""
### {area}
📌 {qtd} links cadastrados
""")
