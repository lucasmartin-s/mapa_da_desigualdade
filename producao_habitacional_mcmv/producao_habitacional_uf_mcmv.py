"""
Producao habitacional MCMV - Brasil por Estado (UF) (2024-2025)
====================================================================
Soma as unidades habitacionais (UH) contratadas nas duas bases do MCMV,
gerando uma linha por Estado (UF).

Gera os totais nacionais no console e exporta para CSV.
"""

import pandas as pd

df_sub = pd.read_csv(r"\mcmv_subsidiado_20260630.csv", sep=";", encoding="utf-8", dtype=str)
df_fin = pd.read_csv(r"\mcmv_financ_sintetico_20260724_v2.csv", sep=";", encoding="utf-8", dtype=str)

# ----------------------------------------------------------------------
# Normalizar tipos e datas
# ----------------------------------------------------------------------
df_sub["dt_assinatura"] = pd.to_datetime(
    df_sub["dt_assinatura"], errors="coerce", dayfirst=True
)
df_sub["ano"] = df_sub["dt_assinatura"].dt.year
df_sub["qtd_uh"] = pd.to_numeric(df_sub["qtd_uh"], errors="coerce")

df_fin["num_ano"] = pd.to_numeric(df_fin["num_ano"], errors="coerce")
df_fin["qtd_uh_financiadas"] = pd.to_numeric(
    df_fin["qtd_uh_financiadas"], errors="coerce"
)

# ----------------------------------------------------------------------
# Extrair e Padronizar UF
# ----------------------------------------------------------------------
df_sub["uf"] = df_sub["txt_sigla_uf"].str.strip().str.upper()
df_fin["uf"] = df_fin["mcmv_fgts_txt_uf"].str.strip().str.upper()

# ----------------------------------------------------------------------
# Filtro (Anos 2024 e 2025)
# ----------------------------------------------------------------------
ANOS = [2024, 2025]

sub_br = df_sub[df_sub["ano"].isin(ANOS)].copy()
fin_br = df_fin[df_fin["num_ano"].isin(ANOS)].copy()

# Remove distratados/cancelados da base subsidiada
sub_br_validas = sub_br[sub_br["txt_situacao_empreendimento"] != "Distratado/Cancelado"]

# ----------------------------------------------------------------------
# Agregar apenas por UF, somando 2024+2025 juntos
# ----------------------------------------------------------------------
sub_por_uf = (
    sub_br_validas.groupby("uf")["qtd_uh"]
    .sum()
    .rename("uh_subsidiadas")
)

fin_por_uf = (
    fin_br.groupby("uf")["qtd_uh_financiadas"]
    .sum()
    .rename("uh_financiadas")
)

# ----------------------------------------------------------------------
# Unir as duas bases
# ----------------------------------------------------------------------
# outer join (concat axis=1) garante que, se uma UF só tiver dados 
# em uma das bases, ela não será perdida
resumo = pd.concat([sub_por_uf, fin_por_uf], axis=1).fillna(0)
resumo = resumo.reset_index()
resumo = resumo.rename(columns={"index": "uf"})

resumo["total_producao"] = resumo["uh_subsidiadas"] + resumo["uh_financiadas"]

for col in ["uh_subsidiadas", "uh_financiadas", "total_producao"]:
    resumo[col] = resumo[col].round().astype(int)

resumo = resumo.sort_values("uf").reset_index(drop=True)

# ----------------------------------------------------------------------
# Exportar para CSV
# ----------------------------------------------------------------------
saida = r"\producao_mcmv_brasil_estados_2024_2025.csv"
resumo.to_csv(saida, sep=";", index=False, encoding="utf-8-sig")