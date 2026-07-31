-- Indicador: Remuneração média dos vínculos formais em ocupações culturais de trabalhadores (sexo masculino), nos municípios do estado do Rio de Janeiro, em 2025
-- Fonte: RAIS 2025 - Base dos Dados
-- Unidade de análise: município
-- Filtro ocupacional: CBO 2002 - lista de ocupações culturais
-- Variável de remuneração: valor_remuneracao_media
-- Data de extração: 2026-07-31

SELECT
    municipio.nome AS nome_municipio,
    rais.id_municipio,
    AVG(rais.valor_remuneracao_media) AS remuneracao_media,
    COUNT(*) AS quantidade_vinculos
FROM `basedosdados.br_me_rais.microdados_vinculos` rais

LEFT JOIN `basedosdados.br_bd_diretorios_brasil.municipio` municipio
ON rais.id_municipio = municipio.id_municipio

WHERE rais.ano = 2025
AND rais.sigla_uf = 'RJ'
AND rais.sexo = '1'

AND rais.cbo_2002 IN (
'131105','131115','262105','262110','262115','262120','262125',
'262130','262135','262205','262210','262215','262220','262235',
'262305','262310','262315','262320','262325','262330',
'262405','262415','262505',
'262605','262610','262615','262620',
'262705','262710',
'262805','262810','262815','262820','262825','262830',
'261205','261305','261310',
'261505','261510','261515','261520','261525','261610',
'261805','261815',
'372105','372110','372115',
'261905','261910',
'373105','373130','373145','373220','373225','373230',
'374405','374410','374415','374420','374425',
'374305','374310',
'374105','374115','374120','374125','374130','374140',
'374145','374150','374155',
'374205','374210','374215',
'371105','371110','371210',
'376105','376110',
'376205','376210','376215','376220','376225','376230',
'376235','376240','376245','376250','376255',
'376310','376325',
'234905','234910','234915',
'231310','232105','234755',
'352405','352420',
'742105','742110','742115','742120','742125','742130',
'742135','742140',
'915205','915210','915215',
'768710',
'791105','791110','791115','791120','791125','791130',
'791135','791140','791145','791150','791155','791160'
)

GROUP BY
    municipio.nome,
    rais.id_municipio

ORDER BY
    nome_municipio;