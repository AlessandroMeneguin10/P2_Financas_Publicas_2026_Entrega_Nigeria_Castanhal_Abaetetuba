"""Gera gráficos exploratórios apenas se a base analítica tiver variáveis compatíveis.
Não inventa indicadores nem converte valores automaticamente."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "codigo_reproducao" / "relatorios_execucao"
OUT.mkdir(parents=True, exist_ok=True)
candidates = [
    ROOT / "data" / "processed" / "BASE_MUNICIPAL_ANALITICA_REAL_2024.csv",
    ROOT / "data" / "processed" / "BASE_MUNICIPAL_CORRIGIDA_P2_2015_2024.csv",
    ROOT / "BASE_MUNICIPAL_ANALITICA_REAL_2024.csv",
    ROOT / "BASE_MUNICIPAL_CORRIGIDA_P2_2015_2024.csv",
    ROOT / "BASE_MUNICIPAL_RECONCILIADA_FINBRA_2015_2024.csv",
]
path = next((p for p in candidates if p.exists()), None)
if path is None:
    raise FileNotFoundError("Base municipal não encontrada. Revise o nome do CSV de entrada.")
df = None
for sep in (";", ",", "\t"):
    try:
        t = pd.read_csv(path, sep=sep, encoding="utf-8-sig", low_memory=False)
        if len(t.columns) > 1:
            df = t
            break
    except Exception:
        pass
if df is None:
    raise ValueError("Não foi possível ler a base municipal.")
print("Base:", path.name)
print("Colunas:", list(df.columns))
# Seleciona somente colunas explicitamente numéricas e não identificadoras.
numeric = df.select_dtypes(include="number").columns.tolist()
numeric = [c for c in numeric if not re.search(r"(^id$|ibge|codigo|código|ano$|year)", str(c), re.I)]
if not numeric:
    print("Nenhuma coluna numérica compatível encontrada. Nenhum gráfico foi criado.")
else:
    report = pd.DataFrame({"variavel_numerica": numeric})
    report.to_csv(OUT / "variaveis_numericas_graficos.csv", index=False, encoding="utf-8-sig")
    # Gráfico de distribuição das primeiras 6 colunas numéricas; diagnóstico, não inferência causal.
    for col in numeric[:6]:
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if series.empty:
            continue
        plt.figure()
        plt.hist(series, bins=20)
        plt.title(f"Distribuição observada: {col}")
        plt.xlabel(col)
        plt.ylabel("Frequência")
        plt.tight_layout()
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(col))[:60]
        plt.savefig(OUT / f"distribuicao_{safe}.png", dpi=160)
        plt.close()
    print(f"Gráficos exploratórios salvos em {OUT}")
