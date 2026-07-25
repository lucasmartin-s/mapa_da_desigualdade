# Mapa da Desigualdade

O Mapa da Desigualdade é uma publicação e uma plataforma de dados desenvolvida pela [Casa Fluminense](https://casafluminense.org.br/) que reúne indicadores socioeconômicos para diagnosticar as desigualdades na Região Metropolitana do Rio de Janeiro (RMRJ). Seu principal objetivo é tornar as desigualdades territoriais visíveis e fornecer evidências para orientar políticas públicas, pesquisas e ações da sociedade civil.

[Na edição mais recente](https://casafluminense.org.br/atuacao/mapa-da-desigualdade/), de 2023, o projeto apresenta 40 indicadores mapeados, organizados em torno de quatro dimensões: Justiça econômica, Justiça racial, Justiça de gênero e Justiça climática, com dados provenientes de diversas bases públicas, privadas e de geração cidadã de dados, mapeando e calculando indicadores comparáveis entre municípios da RMRJ, o Estado do Rio de Janeiro e o Brasil, tornando visíveis disparidades que muitas vezes ficam escondidas em médias nacionais ou estaduais.

Os indicadores abrangem diferentes áreas temáticas: habitação, emprego, transporte, segurança, saneamento, saúde, educação, cultura, assistência social e gestão pública.

## Sobre o repositório

Este repositório é referente apenas a alguns dos dados mais complexos do Mapa da Desigualdade 2026, que exigem a utilização de código para leitura e análise. Por isso, inclui apenas alguns dos indicadores presentes na nova versão do projeto.

## Indicadores disponíveis

### 🌡️ [Salas de Aula Climatizadas](./salas_de_aula_climatizadas)
Percentual de salas de aula climatizadas e com acessibilidade em escolas públicas em funcionamento, a partir dos microdados do Censo Escolar (INEP).

### 📶 [Sem Internet em Casa](./sem_internet_em_casa)
Cobertura de acesso à internet domiciliar entre inscritos do ENEM, segmentada por raça/cor, a partir dos microdados de participantes do ENEM (INEP).

> Cada pasta contém seu próprio README com a metodologia detalhada, o código utilizado e a estrutura dos dados de saída.

## Estrutura do repositório

```
mapa_da_desigualdade/
├── README.md                          ← este arquivo
├── salas_de_aula_climatizadas/
│   ├── salas_de_aula_climatizadas.py
│   └── README.md
├── sem_internet_em_casa/
│   ├── sem_internet_em_casa.py
│   └── README.md
└── ...                                 ← futuros indicadores
```

## Fontes de dados

Todos os dados utilizados são públicos e disponibilizados pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP):

- [Microdados do Censo Escolar](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)
- [Microdados do ENEM](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)

## Metodologia geral

Os indicadores são calculados por meio de contagem direta de registros administrativos declarados pelas escolas ou pelos próprios inscritos, sem ponderação amostral. Por isso, os resultados refletem o universo de respondentes/escolas em cada base, e não necessariamente o total da população residente ou matriculada em cada localidade. Municípios com número reduzido de registros devem ter seus resultados interpretados com cautela.

Detalhes metodológicos específicos de cada indicador estão documentados no README da respectiva pasta.

## Tecnologias utilizadas

- Python (pandas)
- Microdados públicos em formato CSV
- Exportação de resultados em Excel (.xlsx)

## Como contribuir

Sugestões de novos indicadores, correções metodológicas ou melhorias no código são bem-vindas. Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## Autoria

Projeto desenvolvido por [Lucas Martins](https://github.com/lucasmartin-s).
