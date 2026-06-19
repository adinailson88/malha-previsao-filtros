# Camada GAM na previsao por filtros

Neste repositorio, GAM e tratado como triagem de viabilidade por recorte, nao como previsao imediata. O catalogo de filtros informa volume bruto por recorte, mas o ajuste GAM exige serie mensal por filtro.

## Papel metodologico

O uso adequado e aplicar GAM somente aos recortes que tiverem cobertura temporal suficiente. Para chamados, a familia recomendada segue o eixo de contagem. Para custos, a familia recomendada segue o eixo de custos. Categorias raras ou recortes com poucos meses observados devem permanecer fora da inferencia.

## Artefatos

- `scripts/gerar_analise_gam.py`: gera o diagnostico local de adequacao.
- `dados/analise_gam.json`: contrato consumido pelo dashboard.
- `dados_csv/analise_gam.csv`: resumo tabular para auditoria e artigo.

## Criterio de leitura

O dashboard deve apresentar a camada GAM como avaliacao de prontidao: quais recortes parecem volumosos, quais ainda precisam de serie mensal e quais nao devem ser modelados. `N_Registros` nao substitui numero de meses observados.

Sem serie temporal filtrada, a conclusao deve ser: Informação insuficiente para verificar.
