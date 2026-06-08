import os
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Portal LAG",
    page_icon="📊",
    layout="wide"
)

# =========================
# ESTILO VISUAL
# =========================
st.markdown("""
<style>
    .stApp {
        background-color: #0b1220;
        color: white;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: white;
        margin-bottom: 0;
    }

    .sub-title {
        font-size: 15px;
        color: #c7cbd1;
        margin-top: 0;
        margin-bottom: 20px;
    }

    .parker-bar {
        height: 6px;
        width: 100%;
        background: linear-gradient(90deg, #ffcc00 0%, #f5b800 100%);
        border-radius: 8px;
        margin-bottom: 22px;
    }

    div[data-testid="stMetric"] {
        background-color: #121a2b;
        border: 1px solid rgba(255, 204, 0, 0.18);
        padding: 14px;
        border-radius: 12px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        background-color: #0f1726;
    }

    .stTextInput > div > div > input {
        background-color: #121a2b;
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.12);
    }

    .portal-note {
        color: #aeb6c2;
        font-size: 13px;
        margin-top: -8px;
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÕES
# =========================
@st.cache_data
def carregar_dados():
    encodings = ["utf-8-sig", "utf-8", "cp1252", "latin1"]
    separadores = [";", ","]

    ultimo_erro = None

    for encoding in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(
                    "portal_links.csv",
                    sep=sep,
                    encoding=encoding
                )

                df.columns = df.columns.str.strip().str.lower()
                df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False, regex=True)]

                if len(df.columns) <= 1:
                    continue

                for col in df.columns:
                    df[col] = df[col].astype(str).str.strip()

                return df

            except Exception as e:
                ultimo_erro = e

    st.error(f"Não foi possível ler o arquivo portal_links.csv. Erro: {ultimo_erro}")
    st.stop()


def normalizar_link(url):
    url = str(url).strip()

    if not url or url.lower() == "nan":
        return None

    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url

    return url


def emoji_area(area):
    mapa = {
        "planejamento": "📅",
        "compras": "🛒",
        "lean": "🏭",
        "qualidade": "✅",
        "pricing": "💲",
        "financeiro": "💰",
        "logistica": "🚚",
        "logística": "🚚",
        "rh": "👥",
        "manutencao": "🛠️",
        "manutenção": "🛠️",
        "engenharia": "⚙️",
        "producao": "🏗️",
        "produção": "🏗️",
        "ti": "💻"
    }
    return mapa.get(str(area).strip().lower(), "📁")


def emoji_tipo(tipo):
    tipo = str(tipo).strip().lower()

    if "power" in tipo:
        return "📊"
    if "sharepoint" in tipo:
        return "🗂️"
    if "excel" in tipo:
        return "📗"
    if "site" in tipo or "portal" in tipo:
        return "🌐"
    if "form" in tipo:
        return "📝"
    return "🔗"


# =========================
# DADOS
# =========================
df = carregar_dados()

colunas_obrigatorias = ["area", "nome", "link"]
faltando = [col for col in colunas_obrigatorias if col not in df.columns]

if faltando:
    st.error(f"Faltam colunas obrigatórias no CSV: {', '.join(faltando)}")
    st.stop()

if "ativo" in df.columns:
    df = df[
        df["ativo"].astype(str).str.strip().str.lower().isin(
            ["sim", "s", "true", "1", "ativo", "yes", "y"]
        )
    ]

df["link"] = df["link"].apply(normalizar_link)

df = df.dropna(subset=["area", "nome", "link"])
df = df[
    (df["area"] != "") &
    (df["nome"] != "") &
    (df["link"] != "")
].copy()

if "tipo" not in df.columns:
    df["tipo"] = ""

# =========================
# HEADER PARKER
# =========================
header_col1, header_col2 = st.columns([1, 6])

with header_col1:
    if os.path.exists("parker_logo.png"):
        st.image("parker_logo.png", width=140)

with header_col2:
    st.markdown('<div class="main-title">Portal LAG</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Acesso rápido aos dashboards, relatórios e links corporativos</div>',
        unsafe_allow_html=True
    )

st.markdown('<div class="parker-bar"></div>', unsafe_allow_html=True)

# =========================
# MÉTRICAS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Áreas", df["area"].nunique())
col2.metric("Links", len(df))

qtd_powerbi = len(
    df[df["tipo"].astype(str).str.contains("power", case=False, na=False)]
)
col3.metric("Power BI", qtd_powerbi)

st.divider()

# =========================
# BUSCA
# =========================
busca = st.text_input("Pesquisar", placeholder="Digite nome, área ou tipo...")
st.markdown(
    '<div class="portal-note">Use a busca para localizar rapidamente dashboards, páginas e relatórios.</div>',
    unsafe_allow_html=True
)

# =========================
# RESULTADOS DE BUSCA
# =========================
if busca:
    resultado = df[
        df["nome"].astype(str).str.contains(busca, case=False, na=False) |
        df["area"].astype(str).str.contains(busca, case=False, na=False) |
        df["tipo"].astype(str).str.contains(busca, case=False, na=False)
    ].sort_values(["area", "nome"])

    st.subheader("Resultados")

    if resultado.empty:
        st.info("Nenhum resultado encontrado.")
    else:
        for _, row in resultado.iterrows():
            icone = emoji_tipo(row["tipo"])
            st.link_button(
                f"{icone} {row['nome']} | {row['area']}",
                row["link"],
                use_container_width=True
            )

# =========================
# LISTAGEM POR ÁREA
# =========================
else:
    areas = sorted(df["area"].dropna().unique())

    for area in areas:
        area_df = df[df["area"] == area].sort_values("nome")
        qtd_area = len(area_df)
        icone_area = emoji_area(area)

        with st.expander(f"{icone_area} {area} ({qtd_area})", expanded=False):
            for _, row in area_df.iterrows():
                icone = emoji_tipo(row["tipo"])
                texto_botao = f"{icone} {row['nome']}"
                st.link_button(
                    texto_botao,
                    row["link"],
                    use_container_width=True
                )
