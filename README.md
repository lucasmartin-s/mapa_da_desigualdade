# Mapa da Desigualdade

O Mapa da Desigualdade é uma publicação e uma plataforma de dados desenvolvida pela [Casa Fluminense](https://casafluminense.org.br/) que reúne indicadores socioeconômicos para diagnosticar as desigualdades na Região Metropolitana do Rio de Janeiro (RMRJ). Seu principal objetivo é tornar as desigualdades territoriais visíveis e fornecer evidências para orientar políticas públicas, pesquisas e ações da sociedade civil.

[Na edição mais recente](https://casafluminense.org.br/atuacao/mapa-da-desigualdade/), de 2023, o projeto apresenta 40 indicadores mapeados, organizados em torno de quatro dimensões: Justiça econômica, Justiça racial, Justiça de gênero e Justiça climática, com dados provenientes de diversas bases públicas, privadas e de geração cidadã de dados, mapeando e calculando indicadores comparáveis entre municípios da RMRJ, o Estado do Rio de Janeiro e o Brasil, tornando visíveis disparidades que muitas vezes ficam escondidas em médias nacionais ou estaduais.

Os indicadores abrangem diferentes áreas temáticas: habitação, emprego, transporte, segurança, saneamento, saúde, educação, cultura, assistência social e gestão pública.

## Sobre o repositório

Este repositório é referente apenas a alguns dos dados mais complexos da nova versão do projeto, de 2026, que exigem a utilização de código para leitura e análise.

## Indicadores disponíveis

### 🌡️ [Salas de Aula Climatizadas](./salas_de_aula_climatizadas)

Percentual de salas de aula climatizadas e com acessibilidade em escolas públicas em funcionamento, a partir dos microdados do Censo Escolar (INEP).

### 📶 [Sem Internet em Casa](./sem_internet_em_casa)

Cobertura de acesso à internet domiciliar entre inscritos do ENEM, segmentada por raça/cor, a partir dos microdados de participantes do ENEM (INEP).

### 🎭 [Indicadores Culturais RAIS](./indicadores_culturais_rais)

Remuneração média e quantidade de vínculos empregatícios formais em ocupações culturais (CBO 2002), segmentados por raça/cor, a partir dos microdados de vínculos da Relação Anual de Informações Sociais (RAIS/MTE), acessados via Base dos Dados.

### 🧒 [Matrículas em Creche](./matriculas_em_creche)

Total de matrículas em creche (0 a 3 anos), por dependência administrativa (Federal, Estadual, Municipal e Privada), agregado por município da RMRJ, total da RMRJ, Estado do Rio de Janeiro e Brasil, a partir dos microdados do Censo Escolar (INEP).

### 🏘️ [Produção Habitacional MCMV](./producao_habitacional_mcmv)

Produção habitacional do Programa Minha Casa, Minha Vida (MCMV) nos 92 municípios do Estado do Rio de Janeiro (2024–2025), consolidando unidades subsidiadas (OGU) e financiadas (FGTS), a partir das bases do Programa MCMV do Ministério das Cidades.

> Cada pasta contém seu próprio README com a metodologia detalhada, o código utilizado e a estrutura dos dados de saída.

## Estrutura do repositório

```
mapa_da_desigualdade/
├── README.md ← este arquivo
├── .gitignore
├── requirements.txt
├── salas_de_aula_climatizadas/
│   ├── salas_de_aula_climatizadas.py
│   └── README.md
├── sem_internet_em_casa/
│   ├── sem_internet_em_casa.py
│   └── README.md
├── indicadores_culturais_rais/
│   ├── sql/
│   │   ├── remuneracao_cultura_total.sql
│   │   ├── remuneracao_cultura_brancos.sql
│   │   └── remuneracao_cultura_negros.sql
│   │   └── remuneracao_cultura_total_rmrj.sql
│   │   └── remuneracao_cultura_homens.sql
│   │   └── remuneracao_cultura_mulheres.sql
│   ├── dicionarios/
│   │   └── cbo_ocupacoes_culturais.csv
│   ├── resultados/
│   │   └── remuneracao_cultura_brancos.csv
│   │   └── remuneracao_cultura_homens.csv
│   │   └── remuneracao_cultura_mulheres.csv
│   │   └── remuneracao_cultura_negros.csv
│   │   └── remuneracao_cultura_total.csv
│   └── README.md
├── matriculas_em_creche/
│   ├── matriculas_em_creche.py
│   └── README.md
├── producao_habitacional_mcmv/
│   ├── base/                          ← dados brutos (não versionados, ver .gitignore)
│   │   ├── mcmv_subsidiado_20260630.csv
│   │   └── mcmv_financ_sintetico_20260724_v2.csv
│   ├── resultados/
│   │   └── producao_mcmv_rj_municipios_2024_2025.csv
│   ├── producao_habitacional_mcmv.py
│   └── README.md
└── ...  ← futuros indicadores
```

> Os arquivos e pastas de dados brutos não versionados (ex.: `producao_habitacional_mcmv/base/`) estão listados no [`.gitignore`](./.gitignore).

## Fontes de dados

Os dados utilizados são públicos, provenientes de diferentes órgãos e plataformas:

- [Microdados do Censo Escolar](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar) — Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)
- [Microdados do ENEM](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) — Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)
- [Microdados de Vínculos da RAIS](https://basedosdados.org/dataset/br-me-rais) — Ministério do Trabalho e Emprego (MTE), acessados via [Base dos Dados](https://basedosdados.org/)
- Bases de Dados do Programa Minha Casa, Minha Vida — Ministério das Cidades

Detalhes metodológicos específicos de cada indicador estão documentados no README da respectiva pasta.

## Tecnologias utilizadas

- Python ([pandas](https://pandas.pydata.org/))
- [openpyxl](https://openpyxl.readthedocs.io/) (exportação de planilhas `.xlsx` formatadas)
- SQL (BigQuery, via Base dos Dados) — consultas armazenadas em `sql/` e executadas manualmente na plataforma do Base dos Dados, com resultados exportados como CSV
- Microdados públicos em formato CSV
- Exportação de resultados em CSV e Excel (`.xlsx`)

## Como rodar

Instale as dependências Python listadas em [`requirements.txt`](./requirements.txt):

```
pip install -r requirements.txt
```

Cada pasta de indicador contém instruções específicas de execução (fontes de dados a baixar, caminhos a ajustar) no seu próprio README.

## Como contribuir

Sugestões de novos indicadores, correções metodológicas ou melhorias no código são bem-vindas. Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## Licença

Este projeto está licenciado sob a licença MIT. Isso significa que qualquer pessoa pode usar, copiar, modificar e redistribuir o código deste repositório, inclusive para fins comerciais, desde que mantida a atribuição de autoria. Veja o arquivo [LICENSE](./LICENSE) para o texto completo.

## Autoria

Projeto desenvolvido por [Lucas Martins](https://github.com/lucasmartin-s).