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
col1.metric("🏢 Áreas", len(dados))
col2.metric("📊 Dashboards", sum(dados.values()))
col3.metric("👥 Usuários", "LAG")
st.divider()
st.subheader("📂 Áreas")
col1, col2, col3 = st.columns(3)
for i, (area, qtd) in enumerate(dados.items()):
   coluna = [col1, col2, col3][i % 3]
coluna.info(f"{area}\n\n📌 {qtd} links cadastrados")
