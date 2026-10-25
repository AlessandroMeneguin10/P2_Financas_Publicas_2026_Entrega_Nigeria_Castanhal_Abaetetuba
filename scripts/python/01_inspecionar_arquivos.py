"""Inspeciona os arquivos de dados do pacote sem alterar os originais."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "codigo_reproducao" / "relatorios_execucao"
OUT.mkdir(parents=True, exist_ok=True)
EXTS = {".csv", ".xlsx", ".xls", ".rds"}

def inspect_csv(path):
    # Tenta separadores comuns e codificações frequentes em bases públicas brasileiras.
    for sep in (";", ",", "\t", "|"):
        try:
            df = pd.read_csv(path, sep=sep, encoding="utf-8-sig", nrows=10, low_memory=False)
            if df.shape[1] > 1:
                return df
        except Exception:
            pass
    return pd.read_csv(path, encoding="latin-1", nrows=10, low_memory=False)

rows = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in EXTS:
        continue
    if any(part.startswith(".") for part in path.parts):
        continue
    try:
        if path.suffix.lower() == ".csv":
            df = inspect_csv(path)
            rows.append({"arquivo": str(path.relative_to(ROOT)), "status": "lido", "colunas_amostra": len(df.columns),
                         "colunas": " | ".join(map(str, df.columns)), "linhas_amostra": len(df)})
        elif path.suffix.lower() in {".xlsx", ".xls"}:
            xls = pd.ExcelFile(path)
            rows.append({"arquivo": str(path.relative_to(ROOT)), "status": "lido", "abas": " | ".join(xls.sheet_names)})
        else:
            rows.append({"arquivo": str(path.relative_to(ROOT)), "status": "RDS: inspecionar com R/readRDS"})
    except Exception as e:
        rows.append({"arquivo": str(path.relative_to(ROOT)), "status": f"ERRO: {type(e).__name__}: {e}"})
pd.DataFrame(rows).to_csv(OUT / "inventario_arquivos.csv", index=False, encoding="utf-8-sig")
print(f"Inventário salvo em: {OUT / 'inventario_arquivos.csv'}")
