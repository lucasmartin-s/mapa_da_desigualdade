# Acesso à Internet — Microdados ENEM 2025

Script em Python que processa os microdados do ENEM 2025 (INEP) e gera uma planilha `.xlsx` com o total de inscritos **com** e **sem** acesso à internet em casa, segmentado por raça/cor (negros e brancos), para:

- Brasil
- Rio de Janeiro (estado)
- Região Metropolitana do Rio de Janeiro (somatório dos 22 municípios)
- Cada um dos 22 municípios da Região Metropolitana do Rio de Janeiro (RMRJ)

## Pré-requisitos

- Python 3.9+
- Bibliotecas:
  ```bash
  pip install pandas openpyxl
  ```

## Dados de entrada

O script espera o arquivo `PARTICIPANTES_2025.csv`, parte dos microdados do ENEM 2025 disponibilizados pelo INEP em [https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).

> O arquivo não está incluído neste repositório por ser muito grande (vários gigabytes) e por conter dados sob os termos de uso do INEP. Baixe-o diretamente do site oficial.

### Colunas utilizadas

| Coluna | Descrição |
|---|---|
| `CO_UF_PROVA` | Código da UF de aplicação da prova (33 = Rio de Janeiro) |
| `NO_MUNICIPIO_PROVA` | Nome do município de aplicação da prova |
| `Q020` | "Em sua casa, existe acesso à internet por rede wi-fi?" — `A` = Não, `B` = Sim |
| `TP_COR_RACA` | Raça/cor do participante — `1` = Branca, `2` = Preta, `3` = Parda |

Negros = soma de `2` (preta) + `3` (parda).

## Configuração

Antes de rodar, ajuste os dois caminhos no início do script:

```python
CAMINHO_ARQUIVO = r"CAMINHO\PARA\PARTICIPANTES_2025.csv"
CAMINHO_SAIDA = r"CAMINHO\PARA\acesso_internet_enem_2025.xlsx"
```

## Como rodar

```bash
python analise_internet_enem_2025.py
```

O script lê apenas as colunas necessárias (`usecols`) para reduzir o uso de memória, já que o arquivo de participantes costuma ter milhões de linhas.

## Saída

O script gera um arquivo `.xlsx` com uma linha por localidade e as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `Localidade` | Brasil, Rio de Janeiro (Estado), cada município da RMRJ, ou RMRJ |
| `Com internet (Total)` | Inscritos com internet em casa (todas as raças) |
| `Sem internet (Total)` | Inscritos sem internet em casa (todas as raças) |
| `Com internet (Negros)` | Inscritos negros (pretos + pardos) com internet em casa |
| `Sem internet (Negros)` | Inscritos negros (pretos + pardos) sem internet em casa |
| `Total inscritos Negros` | Total de inscritos negros na localidade |
| `Com internet (Brancos)` | Inscritos brancos com internet em casa |
| `Sem internet (Brancos)` | Inscritos brancos sem internet em casa |
| `Total inscritos Brancos` | Total de inscritos brancos na localidade |
| `Total geral de inscritos` | Total de inscritos na localidade (todas as raças) |

A linha `RMRJ` é o somatório das colunas numéricas dos 22 municípios listados abaixo.

## Municípios da Região Metropolitana do Rio de Janeiro (RMRJ)

Composição oficial conforme a Lei Complementar nº 184/2018 (RJ), 22 municípios:

Belford Roxo, Cachoeiras de Macacu, Duque de Caxias, Guapimirim, Itaboraí, Itaguaí, Japeri, Magé, Maricá, Mesquita, Nilópolis, Niterói, Nova Iguaçu, Paracambi, Petrópolis, Queimados, Rio Bonito, Rio de Janeiro, São Gonçalo, São João de Meriti, Seropédica, Tanguá.

## Observações

- O filtro por município é combinado com `CO_UF_PROVA == 33` para evitar contar municípios homônimos de outros estados (ex.: municípios com o mesmo nome fora do RJ).
- O encoding padrão usado é `latin-1` (ISO-8859-1), comum nos microdados do INEP. Caso o arquivo baixado esteja em outro encoding, ajuste o parâmetro `encoding` na leitura do CSV.