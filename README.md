# Malha Previsao por Filtros

Repositorio do eixo de previsao por filtros do ecossistema Malha IA. O objetivo e separar o motor pesado que executa recortes por campus, tipo e categoria, mantendo o `malha-ia` como hub central dos dados.

Repositorio-hub de dados: [adinailson88/malha-ia](https://github.com/adinailson88/malha-ia)  
Dashboard previsto: `https://adinailson88.github.io/malha-previsao-filtros/`

## Escopo

Este repositorio cobre o eixo de filtros:

1. catalogo de filtros disponiveis;
2. motor `motor_previsao_filtros.py`;
3. workflow pesado `previsao_filtros.yml`;
4. exportacao opcional de abas filtradas via Apps Script;
5. dashboard de acompanhamento dos filtros.

Ficam fora deste repositorio:

1. base bruta completa `CHAMADOS`;
2. dashboard global de chamados;
3. previsao global de custos;
4. ODS/ESG;
5. classificacao/reclassificacao de chamados.

## Componentes

1. `motor_previsao_filtros.py`: motor Python para previsoes por filtros.
2. `dados/filtros_disponiveis.json`: catalogo de filtros e sufixos de abas.
3. `dados/contexto_sazonal.json`: contexto sazonal comum ao pipeline.
4. `dados/area_manutencao.json`: contexto institucional de area.
5. `scripts/baixar_dados_hub.py`: baixa snapshots leves do hub.
6. `scripts/exportar_dados_csv.py`: gera CSVs do catalogo e contextos.
7. `scripts/exportar_dados_filtrados_json.py`: exporta abas filtradas via Google Sheets API, quando existirem.
8. `.github/workflows/previsao_filtros.yml`: workflow pesado com Google Sheets.
9. `.github/workflows/atualizar-dados-hub.yml`: workflow leve para atualizar catalogos.
10. `dashboard.html`: painel estatico do catalogo de filtros.

## Execucao local

```powershell
python scripts\baixar_dados_hub.py
python scripts\exportar_dados_csv.py
```

Validacao sintatica:

```powershell
python -m py_compile motor_previsao_filtros.py scripts\baixar_dados_hub.py scripts\exportar_dados_csv.py scripts\exportar_dados_filtrados_json.py
```

Exportar abas filtradas via Google Sheets API, quando ja tiverem sido geradas na planilha:

```powershell
python scripts\exportar_dados_filtrados_json.py --spreadsheet-id ID_DA_PLANILHA --incluir-filtradas
python scripts\exportar_dados_csv.py
```

Executar recalculo completo contra Google Sheets:

```powershell
python motor_previsao_filtros.py --apenas-filtros
```

## Secret necessario para o modo pesado

O workflow `previsao_filtros.yml` precisa do secret:

`AUTENTICACAO_GOOGLE`

O valor esperado e o JSON da conta de servico convertido para Base64, pois o workflow reconstrui `autenticacao_google.json` com `base64 -d`.

## Modo leve e modo pesado

Modo leve:

1. importa `filtros_disponiveis.json`, `contexto_sazonal.json` e `area_manutencao.json` do hub;
2. publica dashboard do catalogo de filtros;
3. nao precisa de API Google Sheets.

Modo pesado:

1. recalcula as previsoes filtradas;
2. cria/atualiza abas `PREVISAO_*{sufixo}` e `PREVISAO_CUSTO_*{sufixo}`;
3. precisa do secret `AUTENTICACAO_GOOGLE`;
4. pode demorar horas, pois multiplica filtros por modelos.

## Licenca

Informação insuficiente para verificar.
