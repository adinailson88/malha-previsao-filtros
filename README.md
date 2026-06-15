# Malha Previsao por Filtros

Repositorio do eixo de previsao por filtros do ecossistema Malha IA. O objetivo e separar o motor pesado que executa recortes por campus, tipo e categoria, mantendo o `malha-ia` como hub central dos dados.

Repositorio-hub de dados: [adinailson88/malha-ia](https://github.com/adinailson88/malha-ia)  
Dashboard previsto: `https://adinailson88.github.io/malha-previsao-filtros/`

## Escopo

Este repositorio cobre o eixo de filtros:

1. catalogo de filtros disponiveis;
2. motor `motor_previsao_filtros.py`;
3. sincronizacao de snapshots publicos do hub;
4. exportacao opcional de abas filtradas via Apps Script, quando necessario;
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
8. `.github/workflows/previsao_filtros.yml`: workflow de compatibilidade que sincroniza dados publicos do hub.
9. `.github/workflows/atualizar-dados-hub.yml`: workflow periodico para atualizar catalogos.
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

## Recalculo autenticado

O recalculo completo contra Google Sheets fica centralizado no repositorio `malha-ia`, que publica os snapshots em `dados/*.json`. Este repositorio nao precisa de `AUTENTICACAO_GOOGLE` para atualizar o dashboard.

## Modo leve e modo pesado

Modo leve:

1. importa `filtros_disponiveis.json`, `contexto_sazonal.json` e `area_manutencao.json` do hub;
2. publica dashboard do catalogo de filtros;
3. nao precisa de API Google Sheets.

Modo autenticado central:

1. recalcula as previsoes filtradas no hub `malha-ia`;
2. cria/atualiza os snapshots publicos em `dados/*.json`;
3. usa credenciais apenas no hub;
4. deixa este repositorio como consumidor estatico dos dados publicados.

## Licenca

Informação insuficiente para verificar.
