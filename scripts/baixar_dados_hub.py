import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen


BASE_URL = "https://raw.githubusercontent.com/adinailson88/malha-ia/main/dados"
ARQUIVOS = [
    "filtros_disponiveis.json",
    "contexto_sazonal.json",
    "area_manutencao.json",
]


def baixar_json(nome: str):
    url = f"{BASE_URL}/{nome}"
    with urlopen(url, timeout=45) as resposta:
        payload = resposta.read().decode("utf-8")
    dados = json.loads(payload)
    if not isinstance(dados, list) or not dados:
        raise ValueError(f"{nome}: formato invalido; esperado matriz JSON com cabecalho")
    return dados, len(payload.encode("utf-8"))


def main() -> int:
    raiz = Path(__file__).resolve().parents[1]
    pasta_dados = raiz / "dados"
    pasta_dados.mkdir(exist_ok=True)

    manifest = {
        "fonte": BASE_URL,
        "atualizado_em_utc": datetime.now(timezone.utc).isoformat(),
        "arquivos": [],
    }

    for nome in ARQUIVOS:
        dados, tamanho_bytes = baixar_json(nome)
        destino = pasta_dados / nome
        destino.write_text(
            json.dumps(dados, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        manifest["arquivos"].append(
            {
                "arquivo": nome,
                "linhas_incluindo_cabecalho": len(dados),
                "linhas_dados": max(len(dados) - 1, 0),
                "bytes_origem": tamanho_bytes,
            }
        )
        print(f"OK {nome}: {max(len(dados) - 1, 0)} linhas")

    (pasta_dados / "manifest_hub.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("OK manifest_hub.json")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
