import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Portal LAG",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    # Tenta identificar separador automaticamente e evita problema de encoding
    df = pd.read_csv(
        "portal_links.csv",
        sep=None,
        engine="python",
        encoding="utf-8-sig"
    )

    # Padroniza nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Remove espaços extras dos valores textuais
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    # Valida colunas obrigatórias
    colunas_obrigatorias = ["area", "nome", "link"]
    faltando = [col for col in colunas_obrigatorias if col not in df.columns]
    if faltando:
        st.error(f"Faltam colunas no CSV: {', '.join(faltando)}")
        st.stop()

    # Filtra ativos de forma mais segura
    if "ativo" in df.columns:
        df = df[
            df["ativo"].astype(str).str.strip().str.lower().isin(
                ["sim", "s", "true", "1", "ativo", "yes", "y"]
            )
        ]

    return df


def normalizar_link(url):
    url = str(url).strip()

    if not url or url.lower() == "nan":
        return None

    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url

    return url


df = carregar_dados()

# Corrige links
df["link"] = df["link"].apply(normalizar_link)

# Remove linhas inválidas
df = df.dropna(subset=["area", "nome", "link"])

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
        df["nome"].astype(str).str.contains(busca, case=False, na=False) |
        df["area"].astype(str).str.contains(busca, case=False, na=False)
    ]

    st.subheader("Resultados")

    for _, row in resultado.sort_values("nome").iterrows():
        st.link_button(
            f"{row['nome']} | {row['area']}",
            row["link"],
            use_container_width=True
        )
else:
    areas = sorted(df["area"].dropna().unique())

    for area in areas:
        with st.expander(area):
            area_df = df[df["area"] == area].sort_values("nome")

            for _, row in area_df.iterrows():
                st.link_button(
                    row["nome"],
                    row["link"],
                    use_container_width=True
                )
