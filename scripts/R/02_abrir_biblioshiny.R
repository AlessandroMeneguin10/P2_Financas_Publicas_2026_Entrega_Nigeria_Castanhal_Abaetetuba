# Abre a interface gráfica Biblioshiny no navegador.
# Execute no R/RStudio: source("codigo_reproducao/R/02_abrir_biblioshiny.R")
if (!requireNamespace("bibliometrix", quietly = TRUE)) {
  install.packages("bibliometrix", repos = "https://cloud.r-project.org")
}
bibliometrix::biblioshiny()
