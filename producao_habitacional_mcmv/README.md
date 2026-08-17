# Produção Habitacional MCMV — Estado do Rio de Janeiro (2024–2025)

Script que consolida a produção habitacional do Programa Minha Casa, Minha Vida (MCMV) nos 92 municípios do estado do Rio de Janeiro, somando os dois principais trilhos de produção do programa: unidades subsidiadas (recursos do OGU) e unidades financiadas (recursos do FGTS).

## Fontes de dados

- **Dados**: [Bases de Dados do Programa Minha Casa, Minha Vida — Ministério das Cidades](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/habitacao/programa-minha-casa-minha-vida/bases-de-dados-do-programa-minha-casa-minha-vida)
- **Dicionário de dados**: [Dicionarios_SNH_2025_10_09.pdf](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/habitacao/arquivos-1/Dicionarios_SNH_2025_10_09.pdf)

Arquivos utilizados:
- `base/mcmv_subsidiado_20260630.csv` — tabela "MCMV-Subsidiado (Empreendimentos)"
- `base/mcmv_financ_sintetico_20260724_v2.csv` — tabela "Contratos do MCMV-Financiado com recursos do FGTS (dados sintéticos)"

> Os CSVs brutos não são versionados neste repositório (ver `.gitignore`). Baixe as versões mais recentes diretamente no link acima antes de rodar o script.

## O que o script faz

1. Lê as duas bases (encoding `utf-8` — os arquivos de origem já vêm em UTF-8; usar `latin1` gera mojibake do tipo `NiterÃ³i`).
2. Normaliza nomes de município (remove acentos, padroniza caixa) para evitar que grafias diferentes entre as duas bases gerem grupos duplicados.
3. Filtra por `UF = RJ` e por ano de contratação (`dt_assinatura` na base subsidiada, `num_ano` na base financiada) — **2024 e 2025**.
4. Exclui da base subsidiada os empreendimentos com `txt_situacao_empreendimento = Distratado/Cancelado`.
5. Agrega por município, somando os dois anos em uma única linha (o ano é usado apenas como filtro, não aparece como coluna de saída).
6. Marca com `RMRJ = sim` os 22 municípios da Região Metropolitana do Rio de Janeiro.
7. Exporta o resultado consolidado em `resultados/producao_mcmv_rj_municipios_2024_2025.csv`.

## Saída

| Coluna | Descrição |
|---|---|
| `municipio` | Nome do município (Title Case, sem acentos) |
| `RMRJ` | `sim`/`nao` — pertence à Região Metropolitana do Rio de Janeiro |
| `uh_subsidiadas` | Unidades habitacionais contratadas via MCMV-Subsidiado (empreendimentos) |
| `uh_financiadas` | Unidades habitacionais contratadas via financiamento individual FGTS |
| `total_producao` | Soma das duas colunas anteriores |

Resultado agregado (estado do RJ, 2024–2025):

| uh_subsidiadas | uh_financiadas | total_producao |
|---|---|---|
| 7.745 | 51.363 | 59.108 |

## Ressalvas metodológicas

Estas decisões afetam a interpretação dos números e devem ser levadas em conta antes de citar os resultados:

- **"Produção" = unidades *contratadas* no período, não entregues.** O filtro usa a data de assinatura/contratação, não a data de conclusão da obra. Uma unidade contratada em 2024 pode ser entregue anos depois. A base subsidiada tem uma coluna de unidades entregues (`qtd_uh_entregues`), mas a base financiada não tem equivalente — por isso o critério de contratação foi usado para as duas, para manter comparabilidade.

- **`uh_subsidiadas` inclui a modalidade FNHIS.** A coluna `txt_modalidade` da base subsidiada contém `Rural`, `RURAL`, `FAR`, `FAR - Compra Assistida`, `Oferta Publica`, `Entidades` e `FNHIS`. O FNHIS (Fundo Nacional de Habitação de Interesse Social) é, por origem legal, um fundo anterior e distinto do MCMV (Lei 11.124/2005, MCMV criado em 2009), mas está presente na mesma base de acompanhamento. No recorte RJ 2024–2025, FNHIS representa **1.924 UH (3,3% do total)** — quase todo o volume nacional de FNHIS no período (1.934 UH) está concentrado no RJ. Optou-se por **manter FNHIS somado em `uh_subsidiadas`**, sem coluna separada, documentando a decisão aqui em vez de segregar no código.

- **Assimetria no filtro de cancelamento.** Só a base subsidiada tem campo de situação do empreendimento (`txt_situacao_empreendimento`), permitindo excluir distratos/cancelamentos. A base financiada (sintética) não tem campo equivalente nas colunas disponíveis — contratos eventualmente distratados nela não são excluídos.

- **Duas fontes de recurso, sem chave única de cruzamento.** As bases não compartilham um identificador comum (CPF do mutuário, código de empreendimento) que permita confirmar com certeza a ausência de dupla contagem. A hipótese de que as bases não se sobrepõem é sustentada por evidência indireta: nenhuma modalidade 100% subsidiada (FAR, Entidades, Oferta Pública, Rural, FNHIS) gera contrapartida em contrato individual de financiamento FGTS — mas isso não foi confirmado em documentação oficial explícita do Ministério das Cidades.

- **Município sem registro no período não aparece com linha zerada.** O resultado tem 87 linhas (não 92) porque municípios sem nenhuma contratação em 2024–2025 (em nenhuma das duas bases) simplesmente não geram linha no agregado, em vez de aparecer com `0`.

- **Região Metropolitana do Rio de Janeiro (RMRJ)** considerada (22 municípios): Belford Roxo, Cachoeiras de Macacu, Duque de Caxias, Guapimirim, Itaboraí, Itaguaí, Japeri, Magé, Maricá, Mesquita, Nilópolis, Niterói, Nova Iguaçu, Paracambi, Petrópolis, Queimados, Rio Bonito, Rio de Janeiro, São Gonçalo, São João de Meriti, Seropédica, Tanguá.

## Como rodar

```bash
python producao_habitacional_mcmv.py
```

Requer `pandas`. Ajuste os caminhos dos CSVs de entrada no início do script conforme a sua estrutura local de pastas.

## Estrutura do projeto

```
producao_habitacional_mcmv/
├── base/                                          # dados brutos (não versionados)
│   ├── mcmv_subsidiado_20260630.csv
│   └── mcmv_financ_sintetico_20260724_v2.csv
├── resultados/
│   └── producao_mcmv_rj_municipios_2024_2025.csv
├── producao_habitacional_mcmv.py
└── README.md
```