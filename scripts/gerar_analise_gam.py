from __future__ import annotations

import csv
import json
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"
CSV_DIR = RAIZ / "dados_csv"
SAIDA_JSON = DADOS / "analise_gam.json"
SAIDA_CSV = CSV_DIR / "analise_gam.csv"
FONTE = DADOS / "filtros_disponiveis.json"


def _num(valor):
    try:
        return int(float(str(valor).replace(",", ".")))
    except (TypeError, ValueError):
        return 0


def _objetos():
    matriz = json.loads(FONTE.read_text(encoding="utf-8"))
    cab = [str(c) for c in matriz[0]]
    return [dict(zip(cab, linha)) for linha in matriz[1:] if linha and linha[0]]


def gerar():
    filtros = _objetos()
    total = len(filtros)
    viable_12 = sum(1 for f in filtros if _num(f.get("N_Registros")) >= 12)
    viable_36 = sum(1 for f in filtros if _num(f.get("N_Registros")) >= 36)
    viable_100 = sum(1 for f in filtros if _num(f.get("N_Registros")) >= 100)
    status = "triagem_de_viabilidade" if total else "sem_dados"
    resultado = {
        "artefato": "analise_gam",
        "eixo": "previsao_filtros",
        "fonte": str(FONTE.relative_to(RAIZ)).replace("\\", "/"),
        "status_geral": status,
        "alvo": "series filtradas futuras por recorte",
        "familia_recomendada": "Herdar familia do alvo: contagem para chamados; Gamma/log ou log1p para custos.",
        "suporte_amostral": {
            "filtros_catalogados": total,
            "recortes_12_mais_registros": viable_12,
            "recortes_36_mais_registros": viable_36,
            "recortes_100_mais_registros": viable_100,
            "minimo_temporal_recomendado": "36 pontos mensais por recorte, nao apenas 36 registros brutos",
        },
        "efeitos_aditivos": [
            {
                "termo": "s(tendencia) por filtro",
                "status": "dependente_de_serie_filtrada",
                "evidencia": "O catalogo informa volume bruto; o ajuste GAM exige serie mensal por sufixo de aba.",
            },
            {
                "termo": "s(mes, cyclic=True)",
                "status": "recomendado_para_recortes_viaveis",
                "evidencia": "Aplicar somente quando o recorte tiver cobertura temporal suficiente.",
            },
            {
                "termo": "hierarquia tipo/categoria",
                "status": "recomendacao_metodologica",
                "evidencia": "Usar filtros como triagem; evitar inferencia em categorias raras.",
            },
        ],
        "recomendacao_dashboard": "Exibir GAM como triagem de recortes aptos, sem criar previsao onde so existe catalogo.",
        "proximas_validacoes": [
            "Materializar series mensais por sufixo de aba antes de ajustar GAM por filtro.",
            "Bloquear ajuste em recortes raros, mesmo que aparecam no catalogo.",
            "Comparar recortes viaveis contra os modelos temporais existentes.",
        ],
        "limites": [
            "N_Registros nao equivale a numero de meses observados.",
            "Sem serie temporal filtrada, usar a frase: Informação insuficiente para verificar.",
        ],
    }
    DADOS.mkdir(exist_ok=True)
    CSV_DIR.mkdir(exist_ok=True)
    SAIDA_JSON.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    with SAIDA_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["campo", "valor"])
        w.writerow(["status_geral", resultado["status_geral"]])
        w.writerow(["filtros_catalogados", total])
        w.writerow(["recortes_12_mais_registros", viable_12])
        w.writerow(["recortes_36_mais_registros", viable_36])
        w.writerow(["recortes_100_mais_registros", viable_100])
    print(f"Gerado {SAIDA_JSON.relative_to(RAIZ)} e {SAIDA_CSV.relative_to(RAIZ)}")


if __name__ == "__main__":
    gerar()
