"""Consolida os relatórios produzidos pelos scripts de validação."""
from pathlib import Path
import pandas as pd
import json
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "codigo_reproducao" / "relatorios_execucao"
OUT.mkdir(parents=True, exist_ok=True)
files = list(OUT.glob("*.csv")) + list(OUT.glob("*.json"))
lines = [
    "# Relatório de execução dos scripts Python",
    "",
    "Este relatório lista arquivos de saída existentes na pasta de execução.",
    "Ele não certifica a completude dos dados nem substitui a conferência das fontes oficiais.",
    ""
]
for p in sorted(files):
    lines.append(f"## {p.name}")
    if p.suffix == ".json":
        try:
            lines += ["```json", json.dumps(json.loads(p.read_text(encoding="utf-8")), ensure_ascii=False, indent=2), "```", ""]
        except Exception as e:
            lines += [f"Não foi possível ler JSON: {e}", ""]
    else:
        try:
            df = pd.read_csv(p, encoding="utf-8-sig", nrows=8)
            lines += [f"Prévia: {len(df.columns)} colunas; mostrando até 8 linhas.", "", df.to_markdown(index=False), ""]
        except Exception as e:
            lines += [f"Não foi possível mostrar prévia: {e}", ""]
(OUT / "RELATORIO_EXECUCAO.md").write_text("\n".join(lines), encoding="utf-8")
print(OUT / "RELATORIO_EXECUCAO.md")
