# Códigos Python e R

## Python
Instale Python 3.10+ e execute a partir da raiz:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/python/01_inspecionar_arquivos.py
python scripts/python/02_validar_bases.py
python scripts/python/03_resumo_bibliometria.py
python scripts/python/04_gerar_graficos_municipais.py
python scripts/python/05_exportar_relatorio_execucao.py
```

Os scripts de inspeção e validação não alteram os dados originais. Ajuste caminhos se necessário. Saídas podem ser gravadas em `codigo_reproducao/relatorios_execucao` por alguns scripts; revise antes de versionar.

## R / Bibliometrix
No RStudio, execute:

```r
source("scripts/R/01_bibliometrix.R")
```

Para abrir Biblioshiny:

```r
source("scripts/R/02_abrir_biblioshiny.R")
```

A análise exige exportação Scopus compatível. Se a importação falhar, confirme os campos e ajuste o caminho. Não trate a presença dos scripts como prova de execução concluída.
