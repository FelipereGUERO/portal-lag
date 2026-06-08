import streamlit as st
st.set_page_config(
   page_title="Portal LAG",
   page_icon="📊",
   layout="wide"
)
st.title("📊 Portal LAG")
st.markdown("### Central de Dashboards e Ferramentas")
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
   st.button("📅 Planejamento")
   st.button("🚚 Logística")
   st.button("🌎 Comex")
with col2:
   st.button("🛒 Compras")
   st.button("⚙️ Lean")
with col3:
   st.button("✅ Qualidade")
   st.button("💰 Pricing")
st.divider()
st.info("Portal em construção 🚀")
