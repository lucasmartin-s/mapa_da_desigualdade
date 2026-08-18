"""
Producao habitacional MCMV - todos os municipios do RJ (2024-2025)
====================================================================

Soma as unidades habitacionais (UH) contratadas nas duas bases do MCMV,
que representam trilhos de producao diferentes (nao se sobrepoem):

  1) mcmv_subsidiado: empreendimentos custeados com OGU
     (modalidades FAR, Entidades, Oferta Publica, Rural)
  2) mcmv_financ_sintetico: contratos individuais financiados com FGTS

Gera uma linha por municipio x ano, com uma coluna "RMRJ" (sim/nao)
indicando se o municipio pertence a Regiao Metropolitana do Rio de Janeiro,
e exporta o resultado para CSV.
"""

import unicodedata
import pandas as pd

df_sub = pd.read_csv("arquivo.csv",
    sep=";",
    encoding="utf-8",
    dtype=str,
)

df_fin = pd.read_csv("arquivo.csv",
    sep=";",
    encoding="utf-8",
    dtype=str,

)

# ----------------------------------------------------------------------
# Normalizar tipos
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
# Funcao auxiliar para normalizar nomes de municipio
#  (remove acentos, caixa alta, espacos nas pontas)
#  evita erro de match por causa de "Niteroi" vs "Niterói", etc.
# ----------------------------------------------------------------------
def normaliza(texto: str) -> str:
    if pd.isna(texto):
        return texto
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    return texto.strip().upper()

df_sub["municipio_norm"] = df_sub["txt_nome_municipio"].apply(normaliza)
df_fin["municipio_norm"] = df_fin["txt_municipio"].apply(normaliza)

# ----------------------------------------------------------------------
# Filtro
# ----------------------------------------------------------------------
UF = "RJ"
ANOS = [2024, 2025]

sub_rj = df_sub[
    (df_sub["txt_sigla_uf"].str.strip().str.upper() == UF)
    & (df_sub["ano"].isin(ANOS))
].copy()

fin_rj = df_fin[
    (df_fin["mcmv_fgts_txt_uf"].str.strip().str.upper() == UF)
    & (df_fin["num_ano"].isin(ANOS))
].copy()

sub_rj_validas = sub_rj[sub_rj["txt_situacao_empreendimento"] != "Distratado/Cancelado"]

# ----------------------------------------------------------------------
# Agregar por municipio, somando 2024+2025 juntos
# ----------------------------------------------------------------------
sub_por_mun = (
    sub_rj_validas.groupby("municipio_norm")["qtd_uh"]
    .sum()
    .rename("uh_subsidiadas")
)

fin_por_mun = (
    fin_rj.groupby("municipio_norm")["qtd_uh_financiadas"]
    .sum()
    .rename("uh_financiadas")
)

# ----------------------------------------------------------------------
# Unir as duas bases (outer join para nao perder municipio que so
#  aparece em uma das duas fontes)
# ----------------------------------------------------------------------
resumo = pd.concat([sub_por_mun, fin_por_mun], axis=1).fillna(0)
resumo = resumo.reset_index()

# nome de exibicao: Title Case e sem acentos/caracteres especiais
# (ex: "SAO GONCALO" -> "Sao Goncalo")
def formata_nome(municipio_norm: str) -> str:
    return municipio_norm.title()

resumo["municipio"] = resumo["municipio_norm"].apply(formata_nome)
resumo["total_producao"] = resumo["uh_subsidiadas"] + resumo["uh_financiadas"]

# valores como inteiro (sem casa decimal)
for col in ["uh_subsidiadas", "uh_financiadas", "total_producao"]:
    resumo[col] = resumo[col].round().astype(int)

# ----------------------------------------------------------------------
# Regiao Metropolitana do Rio de Janeiro (RMRJ)
# ----------------------------------------------------------------------
municipios_rmrj = [
    "Belford Roxo", "Cachoeiras de Macacu", "Duque de Caxias", "Guapimirim",
    "Itaboraí", "Itaguaí", "Japeri", "Magé", "Maricá", "Mesquita",
    "Nilópolis", "Niterói", "Nova Iguaçu", "Paracambi", "Petrópolis",
    "Queimados", "Rio Bonito", "Rio de Janeiro", "São Gonçalo",
    "São João de Meriti", "Seropédica", "Tanguá",
]
municipios_rmrj_norm = {normaliza(m) for m in municipios_rmrj}

resumo["RMRJ"] = resumo["municipio_norm"].apply(
    lambda m: "sim" if m in municipios_rmrj_norm else "nao"
)

# ----------------------------------------------------------------------
# Organizar colunas finais e exportar
# ----------------------------------------------------------------------
resumo = resumo[
    ["municipio", "RMRJ", "uh_subsidiadas", "uh_financiadas", "total_producao"]
].sort_values("municipio").reset_index(drop=True)

# checagem: confere se os 22 municipios da RMRJ foram todos encontrados na base
encontrados = set(resumo.loc[resumo["RMRJ"] == "sim", "municipio"].apply(normaliza))
faltando = municipios_rmrj_norm - encontrados
if faltando:
    print(f"Aviso: {len(faltando)} municipios da RMRJ nao encontrados nas bases: {faltando}")

saida = r"\producao_mcmv_rj_municipios_2024_2025.csv"
resumo.to_csv(saida, sep=";", index=False, encoding="utf-8-sig")
print(f"Arquivo exportado: {saida}")
print(resumo.head(20))
print(f"\nTotal de linhas: {len(resumo)}")
print(f"Total geral de UH (2024-2025): {int(resumo['total_producao'].sum())}")

# ----------------------------------------------------------------------
# Checagens extras de qualidade
# ----------------------------------------------------------------------
print(f"\nMunicipios distintos (base subsidiada, RJ): {sub_rj['municipio_norm'].nunique()}")
print(f"Municipios distintos (base financiada, RJ): {fin_rj['municipio_norm'].nunique()}")
print(f"Municipios distintos no resultado final: {resumo['municipio'].nunique()}")
print(f"Linhas marcadas RMRJ = 'sim': {(resumo['RMRJ'] == 'sim').sum()} (esperado: 22)")
