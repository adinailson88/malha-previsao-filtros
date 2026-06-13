"""
Exportador opcional para snapshots filtrados da planilha Google.

Uso esperado no ambiente que possuir AUTENTICACAO_GOOGLE:
  python scripts/exportar_dados_filtrados_json.py --spreadsheet-id ID --incluir-filtradas

Este script nao baixa CHAMADOS. Ele exporta apenas abas de catalogo e previsoes
filtradas necessarias ao modulo de previsao por filtros.
"""

import argparse
import json
import os
import sys
from pathlib import Path


ABAS_BASE = {
    "FILTROS_DISPONIVEIS": "filtros_disponiveis.json",
    "CONTEXTO_SAZONAL": "contexto_sazonal.json",
    "Área Manutenção": "area_manutencao.json",
}

PREFIXOS_FILTRAVEIS = [
    "PREVISAO_TEMPORAL",
    "PREVISAO_DETALHES",
    "PREVISAO_INCERTEZAS",
    "PREVISAO_DIAGNOSTICO",
    "PREVISAO_RESIDUOS",
    "PREVISAO_QQPLOT",
    "PREVISAO_VALIDACAO",
    "PREVISAO_PRESSUPOSTOS",
    "PREVISAO_CUSTO_TEMPORAL",
    "PREVISAO_CUSTO_DETALHES",
    "PREVISAO_CUSTO_INCERTEZAS",
    "PREVISAO_CUSTO_VALIDACAO",
]


def nome_arquivo_aba(nome_aba: str) -> str:
    nome = (
        nome_aba.lower()
        .replace("ç", "c")
        .replace("ã", "a")
        .replace("á", "a")
        .replace("à", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ú", "u")
    )
    permitido = []
    for char in nome:
        permitido.append(char if char.isalnum() else "_")
    return "_".join("".join(permitido).split("_")).strip("_") + ".json"


def carregar_cliente():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as exc:
        raise RuntimeError("Dependencias ausentes: instale gspread e google-auth") from exc

    credenciais_raw = os.environ.get("AUTENTICACAO_GOOGLE")
    if not credenciais_raw:
        raise RuntimeError("Secret AUTENTICACAO_GOOGLE ausente")
    info = json.loads(credenciais_raw)
    escopos = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    credenciais = Credentials.from_service_account_info(info, scopes=escopos)
    return gspread.authorize(credenciais)


def deve_exportar(nome_aba: str, incluir_filtradas: bool) -> bool:
    if nome_aba in ABAS_BASE:
        return True
    if not incluir_filtradas:
        return False
    return any(nome_aba == prefixo or nome_aba.startswith(prefixo + "__") for prefixo in PREFIXOS_FILTRAVEIS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spreadsheet-id", required=True)
    parser.add_argument("--saida", default="dados")
    parser.add_argument("--incluir-filtradas", action="store_true")
    args = parser.parse_args()

    raiz = Path(__file__).resolve().parents[1]
    pasta_saida = (raiz / args.saida).resolve()
    pasta_saida.mkdir(exist_ok=True)

    cliente = carregar_cliente()
    planilha = cliente.open_by_key(args.spreadsheet_id)

    total = 0
    for aba in planilha.worksheets():
        nome = aba.title
        if not deve_exportar(nome, args.incluir_filtradas):
            continue
        valores = aba.get_all_values()
        arquivo = ABAS_BASE.get(nome, nome_arquivo_aba(nome))
        (pasta_saida / arquivo).write_text(
            json.dumps(valores, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        total += 1
        print(f"OK {nome} -> {arquivo}: {max(len(valores) - 1, 0)} linhas")

    print(f"OK abas exportadas: {total}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
