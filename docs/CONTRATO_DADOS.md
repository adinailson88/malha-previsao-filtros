# Contrato de dados - previsao por filtros

## Fonte central

O repositorio `adinailson88/malha-ia` permanece como hub central dos dados. Este repositorio usa snapshots leves para catalogar filtros e, quando disponivel, snapshots filtrados exportados da planilha.

## Arquivos leves

| Arquivo JSON | Papel |
|---|---|
| `dados/filtros_disponiveis.json` | Lista de filtros, labels, sufixos de abas e quantidade de registros |
| `dados/contexto_sazonal.json` | Contexto de sazonalidade usado pelos motores |
| `dados/area_manutencao.json` | Area construida e area total como contexto institucional |
| `dados/manifest_hub.json` | Metadados de sincronizacao com o hub |

## Campos do catalogo de filtros

| Campo | Significado |
|---|---|
| `Tipo_Filtro` | Grupo do filtro: global, campus, tipo, cat_prev ou cat_corr |
| `Label` | Nome legivel do filtro |
| `Sufixo_Aba` | Sufixo usado nas abas da planilha |
| `N_Registros` | Quantidade de chamados do recorte |

## Abas filtradas esperadas

Quando o workflow pesado ou o exportador via Apps Script forem executados, os nomes seguem o padrao:

| Prefixo | Uso |
|---|---|
| `PREVISAO_TEMPORAL{sufixo}` | Previsao de quantidade de chamados por filtro |
| `PREVISAO_DETALHES{sufixo}` | Parametros e detalhes dos modelos por filtro |
| `PREVISAO_INCERTEZAS{sufixo}` | Intervalos e incertezas por filtro |
| `PREVISAO_VALIDACAO{sufixo}` | Validacao temporal por filtro |
| `PREVISAO_CUSTO_TEMPORAL{sufixo}` | Previsao de custos por filtro |
| `PREVISAO_CUSTO_DETALHES{sufixo}` | Detalhes dos modelos de custo por filtro |
| `PREVISAO_CUSTO_INCERTEZAS{sufixo}` | Incertezas de custo por filtro |
| `PREVISAO_CUSTO_VALIDACAO{sufixo}` | Validacao de custo por filtro |

## Regra de fronteira

`CHAMADOS` nao deve ser duplicado aqui como fonte primaria. Quando for necessario recalcular filtros, usar o fluxo autenticado do hub `malha-ia`; este repositorio consome os snapshots publicos resultantes.

## API e secret

Os workflows deste repositorio nao precisam de API Google Sheets nem de `AUTENTICACAO_GOOGLE`. A credencial Google, quando necessaria, fica restrita ao hub `malha-ia`.

## Limitacoes

O hub atual fornece o catalogo de filtros, mas nao necessariamente publica todos os snapshots filtrados no diretorio `dados/`. A geracao completa depende do workflow pesado ou da exportacao via Apps Script.
