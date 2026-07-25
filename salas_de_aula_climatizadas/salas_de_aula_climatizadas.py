import pandas as pd

CAMINHO_ARQUIVO = r"\Tabela_Escola_2025.csv"
CAMINHO_SAIDA = r"\salas_climatizadas_2025.xlsx" 

SG_UF_RJ = "RJ"

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

df = pd.read_csv(CAMINHO_ARQUIVO, sep=';', encoding='latin-1', low_memory=False)

df_filtrado = df[
    (df['TP_DEPENDENCIA'].isin([1, 2, 3])) &
    (df['TP_SITUACAO_FUNCIONAMENTO'] == 1)
].copy()

def calcular_metricas(sub_df, nome):
    total_utilizadas = sub_df['QT_SALAS_UTILIZADAS'].sum()
    total_climatizadas = sub_df['QT_SALAS_UTILIZA_CLIMATIZADAS'].sum()
    total_acessiveis = sub_df['QT_SALAS_UTILIZADAS_ACESSIVEIS'].sum()

    pct_climatizadas = (total_climatizadas / total_utilizadas * 100) if total_utilizadas > 0 else 0
    pct_acessiveis = (total_acessiveis / total_utilizadas * 100) if total_utilizadas > 0 else 0

    return {
        'Localidade': nome,
        'Total Salas Utilizadas': total_utilizadas,
        'Total Salas Climatizadas': total_climatizadas,
        '% Salas Climatizadas': round(pct_climatizadas, 2),
        'Total Salas Acessíveis': total_acessiveis,
        '% Salas Acessíveis': round(pct_acessiveis, 2),
    }

linhas_municipios = []
for municipio in MUNICIPIOS_RMRJ:
    sub_df = df_filtrado[
        (df_filtrado['NO_MUNICIPIO'] == municipio) &
        (df_filtrado['SG_UF'] == SG_UF_RJ)
    ]
    linhas_municipios.append(calcular_metricas(sub_df, municipio))

df_rmrj = df_filtrado[
    (df_filtrado['NO_MUNICIPIO'].isin(MUNICIPIOS_RMRJ)) &
    (df_filtrado['SG_UF'] == SG_UF_RJ)
]
linha_rmrj = calcular_metricas(df_rmrj, 'RMRJ (Total)')

df_rj = df_filtrado[df_filtrado['SG_UF'] == SG_UF_RJ]
linha_rj = calcular_metricas(df_rj, 'Estado do Rio de Janeiro')

linha_brasil = calcular_metricas(df_filtrado, 'Brasil')

tabela_final = pd.DataFrame(
    linhas_municipios + [linha_rmrj, linha_rj, linha_brasil]
)

tabela_final.to_excel(CAMINHO_SAIDA, sheet_name='Salas Climatizadas', index=False)

print("Arquivo gerado com sucesso em:", CAMINHO_SAIDA)
print(tabela_final)
