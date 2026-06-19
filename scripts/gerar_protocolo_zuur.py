#!/usr/bin/env python3
"""Gera diagnostico de exploracao de dados segundo Zuur et al. (2010)."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"
CSV_DIR = RAIZ / "dados_csv"
SAIDA_JSON = DADOS / "protocolo_zuur.json"
SAIDA_CSV = CSV_DIR / "protocolo_zuur.csv"

REFERENCIA = (
    "Zuur, A.F., Ieno, E.N. & Elphick, C.S. (2010). A protocol for data "
    "exploration to avoid common statistical problems. Methods in Ecology and "
    "Evolution, 1(1), 3-14. doi:10.1111/j.2041-210X.2009.00001.x"
)


def carregar(nome: str) -> list:
    caminho = DADOS / nome
    if not caminho.exists():
        return []
    return json.loads(caminho.read_text(encoding="utf-8"))


def numero(valor) -> float | None:
    try:
        return float(str(valor).replace(".", "").replace(",", "."))
    except (TypeError, ValueError):
        return None


def linhas_tabela(tabela: list) -> tuple[list[str], list[list]]:
    if not tabela or not isinstance(tabela[0], list):
        return [], []
    return [str(c) for c in tabela[0]], [r for r in tabela[1:] if any(str(c).strip() for c in r)]


def iqr(valores: list[float]) -> dict:
    xs = sorted(v for v in valores if v is not None)
    if not xs:
        return {"n": 0, "status": "Informação insuficiente para verificar."}
    def pct(p: float) -> float:
        pos = (len(xs) - 1) * p
        lo = int(pos)
        hi = min(lo + 1, len(xs) - 1)
        frac = pos - lo
        return xs[lo] * (1 - frac) + xs[hi] * frac
    q1, q3 = pct(0.25), pct(0.75)
    dist = q3 - q1
    li, ls = q1 - 1.5 * dist, q3 + 1.5 * dist
    return {"n": len(xs), "min": xs[0], "q1": round(q1, 2), "q3": round(q3, 2), "max": xs[-1], "outliers_baixos": sum(1 for v in xs if v < li), "outliers_altos": sum(1 for v in xs if v > ls)}


def main() -> int:
    filtros = carregar("filtros_disponiveis.json")
    contexto = carregar("contexto_sazonal.json")
    area = carregar("area_manutencao.json")

    cab, linhas = linhas_tabela(filtros)
    tipo_idx = cab.index("Tipo_Filtro") if "Tipo_Filtro" in cab else None
    n_idx = cab.index("N_Registros") if "N_Registros" in cab else None
    registros = [numero(r[n_idx]) for r in linhas if n_idx is not None and len(r) > n_idx]
    registros = [v for v in registros if v is not None]
    por_tipo: dict[str, int] = {}
    if tipo_idx is not None:
        for r in linhas:
            if len(r) > tipo_idx:
                por_tipo[str(r[tipo_idx])] = por_tipo.get(str(r[tipo_idx]), 0) + 1

    faltantes = [
        "dados/previsao_temporal__<sufixo>.json",
        "dados/previsao_detalhes__<sufixo>.json",
        "dados/previsao_incertezas__<sufixo>.json",
        "dados/previsao_validacao__<sufixo>.json",
        "dados/previsao_custo_temporal__<sufixo>.json",
    ]

    passos = [
        {"passo": 1, "titulo": "Outliers em tamanhos dos recortes", "status": "verificado", "evidencia": "dados/filtros_disponiveis.json", "resultado": iqr(registros), "mudanca_minima": "Marcar filtros muito pequenos antes de rodar modelos por recorte."},
        {"passo": 2, "titulo": "Homogeneidade de variancia", "status": "precisa calcular", "evidencia": "snapshots filtrados ainda nao publicados", "resultado": {"status": "Informação insuficiente para verificar."}, "mudanca_minima": "Calcular variancia por serie filtrada quando os JSONs filtrados forem exportados."},
        {"passo": 3, "titulo": "Normalidade", "status": "precisa calcular", "evidencia": "snapshots filtrados ainda nao publicados", "resultado": {"status": "Informação insuficiente para verificar."}, "mudanca_minima": "Publicar pressupostos por sufixo ou usar diagnostico do motor filtrado."},
        {"passo": 4, "titulo": "Zeros ou filtros raros", "status": "verificado", "evidencia": "dados/filtros_disponiveis.json", "resultado": {"filtros_total": len(linhas), "filtros_com_menos_12_registros": sum(1 for v in registros if v < 12), "por_tipo": por_tipo}, "mudanca_minima": "Impedir leitura preditiva forte em filtros abaixo do minimo temporal."},
        {"passo": 5, "titulo": "Colinearidade entre covariaveis", "status": "precisa calcular", "evidencia": "contexto sazonal + snapshots filtrados", "resultado": {"status": "Informação insuficiente para verificar."}, "mudanca_minima": "Reaproveitar VIF do motor quando cada sufixo tiver serie suficiente."},
        {"passo": 6, "titulo": "Relacoes entre Y e X", "status": "parcial", "evidencia": "dados/contexto_sazonal.json", "resultado": {"linhas_contexto": max(0, len(contexto) - 1) if isinstance(contexto, list) else 0}, "mudanca_minima": "Cruzar contexto sazonal com cada serie filtrada publicada."},
        {"passo": 7, "titulo": "Interacoes", "status": "verificado", "evidencia": "dados/filtros_disponiveis.json", "resultado": {"por_tipo": por_tipo}, "mudanca_minima": "Tratar interacao como campus/tipo/categoria, preservando o eixo de filtros."},
        {"passo": 8, "titulo": "Independencia temporal", "status": "precisa calcular", "evidencia": "snapshots filtrados ainda nao publicados", "resultado": {"linhas_area": max(0, len(area) - 1) if isinstance(area, list) else 0}, "mudanca_minima": "Publicar validacao rolling-origin por sufixo quando os resultados filtrados existirem."},
    ]

    out = {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "repositorio": "malha-previsao-filtros",
        "eixo": "previsao por filtros",
        "referencia": REFERENCIA,
        "escopo": "Exploracao do catalogo de filtros e contextos publicos; sem resultados filtrados pesados.",
        "diagnostico_do_que_falta": faltantes,
        "passos": passos,
        "metodo_artigo": (
            "No eixo de filtros, o protocolo de Zuur et al. (2010) deve ser usado como triagem "
            "antes de interpretar previsoes por campus, tipo ou categoria. O tamanho do recorte, "
            "zeros estruturais e independencia temporal determinam se um filtro pode sustentar "
            "modelo preditivo. Enquanto o repositorio estiver no modo leve, o diagnostico fica "
            "restrito ao catalogo de filtros e aos contextos publicados."
        ),
    }

    SAIDA_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    CSV_DIR.mkdir(exist_ok=True)
    with SAIDA_CSV.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(["passo", "titulo", "status", "evidencia", "mudanca_minima"])
        for p in passos:
            writer.writerow([p["passo"], p["titulo"], p["status"], p["evidencia"], p["mudanca_minima"]])
    print(f"OK {SAIDA_JSON}")
    print(f"OK {SAIDA_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
