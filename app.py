import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Portal LAG",
    layout="wide"
)

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

                # Padroniza nomes das colunas
                df.columns = df.columns.str.strip().str.lower()

                # Remove colunas inúteis do tipo "unnamed"
                df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False, regex=True)]

                # Se leu tudo em uma coluna só, tenta outro formato
                if len(df.columns) <= 1:
                    continue

                # Limpa espaços dos valores
                for col in df.columns:
                    df[col] = df[col].astype(str).str.strip()

                return df

            except Exception as e:
                ultimo_erro = e

    st.error(f"Não foi possível ler o arquivo portal_links.csv. Verifique o separador e a codificação. Erro: {ultimo_erro}")
    st.stop()


def normalizar_link(url):
    url = str(url).strip()

    if not url or url.lower() == "nan":
        return None

    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url

    return url


df = carregar_dados()

# Validação de colunas obrigatórias
colunas_obrigatorias = ["area", "nome", "link"]
faltando = [col for col in colunas_obrigatorias if col not in df.columns]

if faltando:
    st.error(f"Faltam colunas obrigatórias no CSV: {', '.join(faltando)}")
    st.stop()

# Filtra apenas links ativos
if "ativo" in df.columns:
    df = df[
        df["ativo"].astype(str).str.strip().str.lower().isin(
            ["sim", "s", "true", "1", "ativo", "yes", "y"]
        )
    ]

# Corrige links
df["link"] = df["link"].apply(normalizar_link)

# Remove linhas inválidas
df = df.dropna(subset=["area", "nome", "link"])
df = df[
    (df["area"] != "") &
    (df["nome"] != "") &
    (df["link"] != "")
]

st.title("Portal LAG")

col1, col2, col3 = st.columns(3)
col1.metric("Areas", df["area"].nunique())
col2.metric("Links", len(df))

if "tipo" in df.columns:
    qtd_powerbi = len(
        df[df["tipo"].astype(str).str.contains("power", case=False, na=False)]
    )
else:
    qtd_powerbi = 0

col3.metric("Power BI", qtd_powerbi)

st.divider()

busca = st.text_input("Pesquisar")

if busca:
    resultado = df[
        df["nome"].astype(str).str.contains(busca, case=False, na=False) |
        df["area"].astype(str).str.contains(busca, case=False, na=False) |
        df["tipo"].astype(str).str.contains(busca, case=False, na=False) if "tipo" in df.columns else False
    ]

    st.subheader("Resultados")

    if resultado.empty:
        st.info("Nenhum resultado encontrado.")
    else:
        for _, row in resultado.sort_values(["area", "nome"]).iterrows():
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

            if area_df.empty:
                st.write("Nenhum link disponível.")
            else:
                for _, row in area_df.iterrows():
                    st.link_button(
                        row["nome"],
                        row["link"],
                        use_container_width=True
                    )
