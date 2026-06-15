# Malha Previsao por Filtros - Instrucoes de Sessao

Ao iniciar qualquer sessao neste repositorio, ler o `README.md` e `docs/CONTRATO_DADOS.md`.

Este repositorio e derivado do hub:
https://github.com/adinailson88/malha-ia

Escopo permitido:

1. Catalogo de filtros.
2. Previsoes por campus, tipo e categoria.
3. Exportacao de abas filtradas.
4. Workflows de sincronizacao dos snapshots publicos.
5. Documentacao do eixo de filtros.

Fora do escopo:

1. Base bruta completa `CHAMADOS`.
2. Classificacao e reclassificacao.
3. ODS/ESG.
4. Previsao global de custos ou chamados sem filtro.

Regra de dados:

`malha-ia` permanece como hub central. Este repositorio deve guardar apenas catalogos, snapshots filtrados e artefatos pertinentes ao eixo de filtros. Nao exigir `AUTENTICACAO_GOOGLE` neste repositorio; o acesso autenticado a planilha fica centralizado no hub.
