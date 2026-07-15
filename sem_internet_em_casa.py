import pandas as pd

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------------------------

CAMINHO_ARQUIVO = r"\PARTICIPANTES_2025.csv" # preencher com o caminho do arquivo CSV de participantes do ENEM 2025
CAMINHO_SAIDA = r"\acesso_internet_enem_2025.xlsx" 

CO_UF_RIO_DE_JANEIRO = 33

MUNICIPIOS_RMRJ = [
    "Belford Roxo",
    "Cachoeiras de Macacu",
    "Duque de Caxias",
    "Guapimirim",
    "Itaboraí",
    "Itaguaí",
    "Japeri",
    "Magé",
    "Maricá",
    "Mesquita",
    "Nilópolis",
    "Niterói",
    "Nova Iguaçu",
    "Paracambi",
    "Petrópolis",
    "Queimados",
    "Rio Bonito",
    "Rio de Janeiro",
    "São Gonçalo",
    "São João de Meriti",
    "Seropédica",
    "Tanguá"
]

COLUNAS = ["CO_UF_PROVA", "NO_MUNICIPIO_PROVA", "Q020", "TP_COR_RACA"]

CODIGO_BRANCA = 1
CODIGOS_NEGROS = [2, 3]  # preta + parda

# ---------------------------------------------------------------------------
# LEITURA DO ARQUIVO
# ---------------------------------------------------------------------------

df = pd.read_csv(
    CAMINHO_ARQUIVO,
    sep=";",
    encoding="latin-1",
    usecols=COLUNAS,
    dtype={
        "CO_UF_PROVA": "Int64",
        "NO_MUNICIPIO_PROVA": "string",
        "Q020": "string",
        "TP_COR_RACA": "Int64",
    },
)

# Tira espaços em branco eventuais nos nomes de município e nas respostas
df["NO_MUNICIPIO_PROVA"] = df["NO_MUNICIPIO_PROVA"].str.strip()
df["Q020"] = df["Q020"].str.strip()

# ---------------------------------------------------------------------------
# FUNÇÃO DE CONTAGEM
# ---------------------------------------------------------------------------

def contar_internet(subconjunto: pd.DataFrame) -> list:
    """Retorna as métricas de acesso à internet (geral, negros e brancos)
    para um recorte do df."""

    com_geral = int((subconjunto["Q020"] == "B").sum())
    sem_geral = int((subconjunto["Q020"] == "A").sum())
    total_geral = len(subconjunto)

    negros = subconjunto[subconjunto["TP_COR_RACA"].isin(CODIGOS_NEGROS)]
    com_negros = int((negros["Q020"] == "B").sum())
    sem_negros = int((negros["Q020"] == "A").sum())
    total_negros = len(negros)

    brancos = subconjunto[subconjunto["TP_COR_RACA"] == CODIGO_BRANCA]
    com_brancos = int((brancos["Q020"] == "B").sum())
    sem_brancos = int((brancos["Q020"] == "A").sum())
    total_brancos = len(brancos)

    return [
        com_geral, sem_geral,
        com_negros, sem_negros, total_negros,
        com_brancos, sem_brancos, total_brancos,
        total_geral,
    ]


COLUNAS_RESULTADO = [
    "Localidade",
    "Com internet (Total)",
    "Sem internet (Total)",
    "Com internet (Negros)",
    "Sem internet (Negros)",
    "Total inscritos Negros",
    "Com internet (Brancos)",
    "Sem internet (Brancos)",
    "Total inscritos Brancos",
    "Total geral de inscritos",
]


# ---------------------------------------------------------------------------
# CÁLCULOS
# ---------------------------------------------------------------------------

resultados = []

# Brasil
resultados.append(["Brasil"] + contar_internet(df))

# Rio de Janeiro (estado)
df_rj = df[df["CO_UF_PROVA"] == CO_UF_RIO_DE_JANEIRO]
resultados.append(["Rio de Janeiro (Estado)"] + contar_internet(df_rj))

# Municípios da RMRJ
linhas_rmrj = []
for municipio in MUNICIPIOS_RMRJ:
    df_mun = df_rj[df_rj["NO_MUNICIPIO_PROVA"] == municipio]
    linha = [municipio] + contar_internet(df_mun)
    linhas_rmrj.append(linha)

resultados.extend(linhas_rmrj)

# Linha de somatório da RMRJ (soma das colunas numéricas dos 22 municípios)
somatorio_rmrj = ["RMRJ"] + [
    sum(linha[i] for linha in linhas_rmrj) for i in range(1, len(COLUNAS_RESULTADO))
]
resultados.append(somatorio_rmrj)

df_resultado = pd.DataFrame(resultados, columns=COLUNAS_RESULTADO)

# ---------------------------------------------------------------------------
# EXPORTAÇÃO
# ---------------------------------------------------------------------------

df_resultado.to_excel(CAMINHO_SAIDA, index=False, sheet_name="Acesso Internet")