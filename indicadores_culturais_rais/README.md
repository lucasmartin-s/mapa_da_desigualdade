# Indicadores do Mercado de Trabalho Cultural — RAIS 2025

## Sobre o projeto

Este repositório contém as consultas SQL utilizadas para a construção de indicadores do mercado de trabalho cultural a partir dos microdados de vínculos da **Relação Anual de Informações Sociais (RAIS)**, disponibilizados pela **Base dos Dados**.

O objetivo é estimar características do emprego formal em ocupações relacionadas ao setor cultural, considerando indicadores como:

* remuneração média dos vínculos empregatícios;
* quantidade de vínculos formais;
* distribuição territorial dos empregos culturais;
* recortes por raça/cor.

A unidade de análise utilizada é o **vínculo empregatício formal**, e não necessariamente o trabalhador individual.

---

## Fonte dos dados

### RAIS — Microdados de Vínculos

Fonte:

* Base dos Dados
* Ministério do Trabalho e Emprego (MTE)

Tabela utilizada:

```
basedosdados.br_me_rais.microdados_vinculos
```

Principais variáveis utilizadas:

| Variável                  | Descrição                                     |
| ------------------------- | --------------------------------------------- |
| `ano`                     | Ano de referência da RAIS                     |
| `id_municipio`            | Código do município do vínculo                |
| `sigla_uf`                | Unidade da Federação                          |
| `cbo_2002`                | Código da ocupação segundo a CBO 2002         |
| `raca_cor`                | Raça/cor declarada no registro administrativo |
| `valor_remuneracao_media` | Remuneração média mensal do vínculo           |

---

## Definição de ocupações culturais

As ocupações culturais foram identificadas a partir de uma seleção de códigos da **Classificação Brasileira de Ocupações (CBO 2002)**.

A lista inclui ocupações relacionadas a:

* produção cultural;
* audiovisual;
* cinema, televisão e rádio;
* música;
* artes cênicas;
* dança;
* patrimônio cultural;
* bibliotecas, arquivos e museus;
* artesanato;
* direitos autorais;
* ensino de artes.

A tabela com os códigos e nomes das ocupações está disponível em:

```
dicionarios/cbo_ocupacoes_culturais.csv
```

Fonte oficial:

Ministério do Trabalho e Emprego — CBO 2002
https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/cbo

---

## Metodologia do indicador

### Remuneração média

A remuneração média foi calculada utilizando a variável:

```
valor_remuneracao_media
```

O cálculo utilizado foi:

```
AVG(valor_remuneracao_media)
```

Como cada registro representa um vínculo empregatício, a média corresponde à média dos salários registrados entre os vínculos culturais selecionados.

---

### Quantidade de vínculos

A quantidade de empregos formais foi estimada por:

```
COUNT(*)
```

Cada linha da RAIS representa um vínculo empregatício.

---

## Recorte territorial

Os indicadores são agregados por município utilizando:

```
id_municipio
```

Os nomes dos municípios são obtidos a partir do diretório:

```
basedosdados.br_bd_diretorios_brasil.municipio
```

---

## Recorte racial

A variável utilizada foi:

```
raca_cor
```

Segundo o dicionário da RAIS:

| Grupo    | Código |
| -------- | ------ |
| Indígena | 1      |
| Branca   | 2      |
| Preta    | 4      |
| Amarela  | 6      |
| Parda    | 8      |
| Ignorado | -1     |

Para os indicadores raciais:

### População branca

Filtro:

```sql
raca_cor = '2'
```

### População negra

Considerada como a soma de pessoas autodeclaradas pretas e pardas:

```sql
raca_cor IN ('4','8')
```

---

## Estrutura do repositório

```
.
├── README.md
│
├── sql/
│   ├── remuneracao_cultura_total.sql
│   ├── remuneracao_cultura_brancos.sql
│   └── remuneracao_cultura_negros.sql
│
├── dicionarios/
│   └── cbo_ocupacoes_culturais.csv
│
└── resultados/
    └── tabelas_indicadores/
```

---

## Limitações metodológicas

* A RAIS registra **vínculos empregatícios**, portanto um mesmo indivíduo pode aparecer mais de uma vez caso possua múltiplos vínculos formais.
* O indicador representa a remuneração média dos vínculos selecionados, e não necessariamente a renda individual dos trabalhadores.
* A identificação do setor cultural depende da seleção de ocupações CBO adotada neste projeto.
* Vínculos sem informação válida de raça/cor podem não ser considerados nos recortes raciais.

---

## Reprodutibilidade

As consultas SQL disponíveis neste repositório permitem reproduzir os indicadores diretamente na infraestrutura do BigQuery utilizando as tabelas públicas da Base dos Dados.

Data de referência dos dados:

```
RAIS 2025
```

Data de elaboração:

```
2026
```