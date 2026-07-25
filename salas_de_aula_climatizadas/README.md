# Salas de Aula Climatizadas — Censo Escolar 2025

Script em Python que calcula indicadores de infraestrutura escolar (salas climatizadas e salas acessíveis) para escolas públicas em funcionamento, com foco na Região Metropolitana do Rio de Janeiro (RMRJ), no Estado do Rio de Janeiro e no Brasil.

## O que o script faz

A partir dos microdados do Censo Escolar (INEP), o script gera uma tabela única contendo:

- **Total de salas utilizadas**
- **Total de salas climatizadas**
- **Percentual de salas climatizadas** (em relação ao total de salas utilizadas)
- **Total de salas com acessibilidade**
- **Percentual de salas acessíveis** (em relação ao total de salas utilizadas)

Essas métricas são calculadas para:

1. Cada um dos 22 municípios da Região Metropolitana do Rio de Janeiro (RMRJ)
2. O somatório da RMRJ como um todo
3. O Estado do Rio de Janeiro
4. O Brasil

## Filtros aplicados

Somente são consideradas **escolas públicas em funcionamento**:

- `TP_DEPENDENCIA` ∈ {1, 2, 3} → Federal, Estadual ou Municipal (exclui escolas privadas, código 4)
- `TP_SITUACAO_FUNCIONAMENTO` = 1 → Em atividade

## Municípios da RMRJ considerados

Belford Roxo, Cachoeiras de Macacu, Duque de Caxias, Guapimirim, Itaboraí, Itaguaí, Japeri, Magé, Maricá, Mesquita, Nilópolis, Niterói, Nova Iguaçu, Paracambi, Petrópolis, Queimados, Rio Bonito, Rio de Janeiro, São Gonçalo, São João de Meriti, Seropédica e Tanguá (22 municípios, conforme legislação vigente da RMRJ).

## Fonte dos dados

Microdados do Censo Escolar da Educação Básica, disponibilizados pelo INEP:
https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar

Arquivo utilizado: `Tabela_Escola_2025.csv`

## Requisitos

```bash
pip install pandas openpyxl
```

- `pandas` — leitura e processamento dos dados
- `openpyxl` — exportação para arquivo `.xlsx`

## Como usar

1. Baixe os microdados do Censo Escolar 2025 no site do INEP e extraia o arquivo `Tabela_Escola_2025.csv`.
2. Ajuste os caminhos no início do script:

```python
CAMINHO_ARQUIVO = r"caminho\para\Tabela_Escola_2025.csv"
CAMINHO_SAIDA = r"caminho\para\salas_climatizadas_2025.xlsx"
```

3. Execute o script:

```bash
python salas_de_aula_climatizadas.py
```

4. O resultado será salvo em `salas_climatizadas_2025.xlsx` e também impresso no terminal.

## Estrutura do arquivo de saída

Uma única planilha (`Salas Climatizadas`) com uma linha por localidade:

| Localidade | Total Salas Utilizadas | Total Salas Climatizadas | % Salas Climatizadas | Total Salas Acessíveis | % Salas Acessíveis |
|---|---|---|---|---|---|
| Belford Roxo | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |
| RMRJ (Total) | ... | ... | ... | ... | ... |
| Estado do Rio de Janeiro | ... | ... | ... | ... | ... |
| Brasil | ... | ... | ... | ... | ... |

## Observações técnicas

- O CSV do INEP usa encoding `latin-1` e separador `;`.
- A coluna `SG_UF` contém a **sigla** da unidade federativa (ex: `"RJ"`), não o código numérico IBGE.
- Percentuais são calculados como `(total_climatizadas ou acessíveis / total_utilizadas) * 100`, retornando `0` quando o total de salas utilizadas é zero (evita divisão por zero).

## Possíveis melhorias futuras

- Adicionar comparação ano a ano (histórico do Censo Escolar).
- Incluir gráficos automáticos (ex: ranking de municípios por % de salas climatizadas).
- Parametrizar a UF/região via linha de comando, tornando o script reutilizável para outras regiões metropolitanas.
