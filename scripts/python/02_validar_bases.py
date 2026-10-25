"""Valida estrutura, duplicatas, ausências e tipos sem corrigir dados silenciosamente."""
from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "codigo_reproducao" / "relatorios_execucao"
OUT.mkdir(parents=True, exist_ok=True)

def read_csv_robust(path):
    for enc in ("utf-8-sig", "latin-1"):
        for sep in (";", ",", "\t", "|"):
            try:
                df = pd.read_csv(path, encoding=enc, sep=sep, low_memory=False)
                if len(df.columns) > 1:
                    return df
            except Exception:
                continue
    raise ValueError("Não foi possível identificar codificação/separador.")

records = []
for path in ROOT.rglob("*.csv"):
    try:
        df = read_csv_robust(path)
        records.append({
            "arquivo": str(path.relative_to(ROOT)),
            "linhas": int(len(df)),
            "colunas": int(len(df.columns)),
            "duplicatas_linha_inteira": int(df.duplicated().sum()),
            "celulas_ausentes": int(df.isna().sum().sum()),
            "colunas_com_ausencia": int((df.isna().sum() > 0).sum()),
            "colunas": " | ".join(map(str, df.columns))
        })
    except Exception as exc:
        records.append({"arquivo": str(path.relative_to(ROOT)), "erro": f"{type(exc).__name__}: {exc}"})

out = pd.DataFrame(records)
out.to_csv(OUT / "validacao_estrutural_csv.csv", index=False, encoding="utf-8-sig")
(OUT / "validacao_estrutural_resumo.json").write_text(
    json.dumps({"arquivos_csv_avaliados": len(records),
                "observacao": "Validação estrutural; não certifica a completude nem a correção substantiva dos dados."},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(out[["arquivo"] + (["linhas", "colunas", "duplicatas_linha_inteira", "celulas_ausentes"] if "linhas" in out.columns else [])].to_string(index=False))
