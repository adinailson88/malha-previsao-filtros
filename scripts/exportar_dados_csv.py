import csv
import json
import sys
from pathlib import Path


ARQUIVOS = [
    "filtros_disponiveis.json",
    "contexto_sazonal.json",
    "area_manutencao.json",
]


def carregar_matriz(caminho: Path):
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(dados, list) or not dados or not isinstance(dados[0], list):
        raise ValueError(f"{caminho.name}: esperado matriz JSON com cabecalho")
    return dados


def exportar_csv(origem: Path, destino: Path) -> int:
    matriz = carregar_matriz(origem)
    destino.parent.mkdir(exist_ok=True)
    with destino.open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(matriz)
    return max(len(matriz) - 1, 0)


def main() -> int:
    raiz = Path(__file__).resolve().parents[1]
    pasta_dados = raiz / "dados"
    pasta_csv = raiz / "dados_csv"
    pasta_csv.mkdir(exist_ok=True)

    for nome in ARQUIVOS:
        origem = pasta_dados / nome
        if not origem.exists():
            raise FileNotFoundError(f"Arquivo ausente: {origem}")
        destino = pasta_csv / nome.replace(".json", ".csv")
        linhas = exportar_csv(origem, destino)
        print(f"OK {destino.relative_to(raiz)}: {linhas} linhas")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
