"""Gera estatísticas descritivas do corpus Scopus, quando os campos estão disponíveis."""
from pathlib import Path
import pandas as pd
import re, json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "codigo_reproducao" / "relatorios_execucao"
OUT.mkdir(parents=True, exist_ok=True)
CANDIDATES = [
    ROOT / "data" / "original" / "bibliometria" / "BASE_80_COM_METADADOS_SCOPUS.csv",
    ROOT / "data" / "original" / "bibliometria" / "SCOPUS_80_ARTIGOS_FILTRADOS.csv",
    ROOT / "BASE_80_COM_METADADOS_SCOPUS.csv",
    ROOT / "SCOPUS_80_ARTIGOS_FILTRADOS(1).csv",
]
source = next((p for p in CANDIDATES if p.exists()), None)
if source is None:
    matches = list(ROOT.rglob("*SCOPUS*.csv")) + list(ROOT.rglob("*80*METADADOS*.csv"))
    source = matches[0] if matches else None
if source is None:
    raise FileNotFoundError("Não localizei o CSV de metadados Scopus. Ajuste CANDIDATES para o arquivo correto.")

df = None
for sep in (";", ",", "\t"):
    try:
        candidate = pd.read_csv(source, sep=sep, encoding="utf-8-sig", low_memory=False)
        if len(candidate.columns) > 2:
            df = candidate
            break
    except Exception:
        pass
if df is None:
    raise ValueError("Não consegui ler o CSV Scopus.")

def find_col(patterns):
    for col in df.columns:
        if any(re.search(p, str(col), re.I) for p in patterns):
            return col
    return None

year_col = find_col([r"^Year$", r"Publication Year", r"PY"])
source_col = find_col([r"^Source title$", r"^SO$", r"Journal"])
doc_type_col = find_col([r"^Document Type$", r"^DT$"])
doi_col = find_col([r"^DOI$", r"^DI$"])
author_col = find_col([r"^Authors$", r"^AU$"])
summary = {
    "arquivo_fonte": str(source.relative_to(ROOT)),
    "registros": int(len(df)),
    "colunas": list(map(str, df.columns)),
    "anos": None,
    "fontes_distintas": None,
    "tipos_documentais": None,
    "dois_distintos": None,
    "autores_distintos_aproximados": None,
    "nota": "Estatísticas dependem dos campos presentes no export. Não equivale à execução do Bibliometrix."
}
if year_col:
    years = pd.to_numeric(df[year_col], errors="coerce").dropna()
    summary["anos"] = {"min": int(years.min()) if len(years) else None,
                       "max": int(years.max()) if len(years) else None}
if source_col:
    summary["fontes_distintas"] = int(df[source_col].nunique(dropna=True))
if doc_type_col:
    summary["tipos_documentais"] = df[doc_type_col].fillna("Ausente").value_counts().to_dict()
if doi_col:
    summary["dois_distintos"] = int(df[doi_col].dropna().astype(str).str.strip().nunique())
if author_col:
    authors = set()
    for cell in df[author_col].dropna().astype(str):
        authors.update(x.strip() for x in re.split(r";|,", cell) if x.strip())
    summary["autores_distintos_aproximados"] = len(authors)
(OUT / "resumo_bibliometria_python.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
