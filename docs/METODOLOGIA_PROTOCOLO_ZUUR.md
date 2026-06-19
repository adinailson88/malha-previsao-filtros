# Protocolo de exploracao de dados - Zuur et al. (2010)

Este eixo usa o protocolo de oito passos de Zuur, Ieno & Elphick (2010) como triagem dos recortes por campus, tipo e categoria antes da interpretacao preditiva.

Referencia: Zuur, A.F., Ieno, E.N. & Elphick, C.S. (2010). A protocol for data exploration to avoid common statistical problems. Methods in Ecology and Evolution, 1(1), 3-14. doi:10.1111/j.2041-210X.2009.00001.x.

Aplicacao no artigo: cada filtro deve ser avaliado quanto a tamanho do recorte, zeros estruturais, outliers de volume, relacao com contexto sazonal e independencia temporal antes de receber interpretacao preditiva. Filtros pequenos devem ser tratados como catalogo operacional, nao como evidencia de forecast.

Artefatos:

1. `scripts/gerar_protocolo_zuur.py`
2. `dados/protocolo_zuur.json`
3. `dados_csv/protocolo_zuur.csv`
4. Bloco "Protocolo de exploracao de dados" em `dashboard.html`

Diagnostico atual: o repositorio esta em modo leve. Faltam snapshots filtrados completos (`previsao_temporal__<sufixo>.json`, detalhes, incertezas, validacao e custos filtrados) para completar os passos que dependem de residuos e validacao temporal.
