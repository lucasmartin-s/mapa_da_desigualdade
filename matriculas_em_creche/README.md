# Matrículas em Creche — RMRJ, Estado do Rio e Brasil

Script Python que calcula o total de matrículas em creche (0 a 3 anos) a
partir dos microdados do Censo Escolar, agregando por:

- Cada um dos 22 municípios da Região Metropolitana do Rio de Janeiro (RMRJ)
- Total da RMRJ
- Total do Estado do Rio de Janeiro
- Total do Brasil

Em cada linha, além do total, as matrículas são detalhadas por tipo de
dependência administrativa: **Federal, Estadual, Municipal e Privada**.

O resultado é exportado em uma planilha `.xlsx` formatada.

## Requisitos

- Python 3.8+
- Bibliotecas: `pandas` e `openpyxl`

Instalar dependências:

```bash
pip install pandas openpyxl
```

## Arquivos de entrada esperados

O script espera dois arquivos CSV do Censo Escolar (INEP), com separador
`;` e encoding `latin-1` (padrão dos microdados):

### `Tabela_Matricula_2025.csv`
Uma linha por escola, contendo pelo menos:

| Coluna | Descrição |
|---|---|
| `CO_ENTIDADE` | Código único da escola |
| `QT_MAT_INF_CRE` | Quantidade de matrículas em creche |

### `Tabela_Escola_2025.csv`
Uma linha por escola, contendo pelo menos:

| Coluna | Descrição |
|---|---|
| `CO_ENTIDADE` | Código único da escola |
| `SG_UF` | Sigla da UF (ex: `RJ`) |
| `NO_MUNICIPIO` | Nome do município |
| `TP_DEPENDENCIA` | Dependência administrativa: `1`=Federal, `2`=Estadual, `3`=Municipal, `4`=Privada |

As duas tabelas são unidas (`merge`) pela chave `CO_ENTIDADE`.

## Como usar

1. Coloque os dois arquivos CSV e o script `gerar_planilha_creche.py` na
   mesma referência de pasta (ou ajuste os caminhos, veja abaixo).
2. Edite as constantes no topo do script, se necessário:

```python
CAMINHO_MATRICULA = r"\Tabela_Matricula_2025.csv"
CAMINHO_ESCOLA    = r"\Tabela_Escola_2025.csv"
ARQUIVO_SAIDA     = r"\matriculas_creche_rmrj_2025.xlsx"
```

   > **Atenção (Windows):** os caminhos no script atual começam com `\`
   > (raiz do drive atual), o que provavelmente não é o que você quer.
   > Use um caminho completo, por exemplo:
   > `C:\Users\SeuUsuario\Documents\dados\Tabela_Matricula_2025.csv`
   > Ou, se os arquivos estiverem na mesma pasta do script, use apenas
   > o nome do arquivo: `"Tabela_Matricula_2025.csv"`.

3. Execute:

```bash
python gerar_planilha_creche.py
```

4. O script imprime a tabela de resultados no terminal e gera o arquivo
   definido em `ARQUIVO_SAIDA`.

## Estrutura da planilha gerada

| Território | Total | Federal | Estadual | Municipal | Privada |
|---|---|---|---|---|---|
| Belford Roxo | ... | ... | ... | ... | ... |
| ... (demais 21 municípios da RMRJ) | | | | | |
| **RMRJ (Total)** | ... | ... | ... | ... | ... |
| **Estado do Rio de Janeiro** | ... | ... | ... | ... | ... |
| **Brasil** | ... | ... | ... | ... | ... |

As três linhas de agregado aparecem em negrito na planilha final.

## Possíveis problemas e como resolver

- **Município aparece com zero matrículas**: o Censo Escolar às vezes
  grafa nomes de município de forma diferente da esperada (acentuação,
  abreviações). Verifique os nomes reais com:
  ```python
  df["NO_MUNICIPIO"].unique()
  ```

- **Erro de encoding ou separador ao ler o CSV**: confirme o separador
  (`;` ou `,`) e o encoding (`latin-1` ou `utf-8`) abrindo o arquivo em
  um editor de texto simples antes de rodar o script.

- **Arquivos em `.xlsx` em vez de `.csv`**: troque `pd.read_csv(...)`
  por `pd.read_excel(...)` nas duas leituras dentro de `carregar_dados()`,
  removendo os parâmetros `sep` e `encoding`.

- **`KeyError` de coluna ausente**: confirme se os nomes de coluna nos
  seus arquivos são exatamente `CO_ENTIDADE`, `QT_MAT_INF_CRE`, `SG_UF`,
  `NO_MUNICIPIO` e `TP_DEPENDENCIA` (o Censo Escolar às vezes atualiza
  nomenclaturas entre edições).

## Municípios da RMRJ considerados

Belford Roxo, Cachoeiras de Macacu, Duque de Caxias, Guapimirim,
Itaboraí, Itaguaí, Japeri, Magé, Maricá, Mesquita, Nilópolis, Niterói,
Nova Iguaçu, Paracambi, Petrópolis, Queimados, Rio Bonito, Rio de
Janeiro, São Gonçalo, São João de Meriti, Seropédica, Tanguá (22 no
total, conforme Lei Complementar Estadual nº 184/2018).