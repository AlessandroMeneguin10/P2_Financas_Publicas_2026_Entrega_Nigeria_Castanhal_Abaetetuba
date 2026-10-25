# Análise bibliométrica reproduzível com Bibliometrix/Biblioshiny
# Ajuste o caminho do CSV exportado do Scopus antes de executar.
# Este script não afirma ter sido executado neste ambiente; rode no R/RStudio local.

required <- c("bibliometrix", "readr", "dplyr", "stringr", "ggplot2")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) {
  install.packages(missing, repos = "https://cloud.r-project.org")
}
library(bibliometrix)
library(readr)
library(dplyr)
library(stringr)
library(ggplot2)

root <- normalizePath(file.path(getwd()), winslash = "/", mustWork = FALSE)
# Caminhos alternativos dentro do pacote:
candidates <- c(
  file.path(root, "BASE_80_COM_METADADOS_SCOPUS.csv"),
  file.path(root, "SCOPUS_80_ARTIGOS_FILTRADOS(1).csv"),
  file.path(root, "ENTREGA_P2_242026481_BIBLIOMETRIA_FINAL", "BASE_80_COM_METADADOS_SCOPUS.csv")
)
input <- candidates[file.exists(candidates)][1]
if (is.na(input)) stop("Não achei o CSV Scopus. Edite 'candidates' com o caminho correto.")

outdir <- file.path(root, "resultados_bibliometrix")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

# Bibliometrix lê o arquivo bruto exportado do Scopus em formato CSV.
# Se a base for um CSV já transformado, os nomes de campos podem não ser os originais Scopus.
M <- tryCatch(convert2df(file = input, dbsource = "scopus", format = "csv"),
              error = function(e) {
                message("convert2df falhou. Confirme que o arquivo é um export original do Scopus: ", e$message)
                stop(e)
              })
write.csv(M, file.path(outdir, "base_convertida_bibliometrix.csv"), row.names = FALSE, fileEncoding = "UTF-8")

res <- biblioAnalysis(M, sep = ";")
sumres <- summary(object = res, k = 20, pause = FALSE)
capture.output(sumres, file = file.path(outdir, "resumo_bibliometrico.txt"))

# Gráficos e tabelas principais:
png(file.path(outdir, "producao_anual.png"), width = 1400, height = 900, res = 150)
plot(x = res, k = 20, pause = FALSE)
dev.off()

# Matrizes temáticas e de coocorrência (se o campo de palavras-chave existir):
if ("DE" %in% names(M) && any(!is.na(M$DE))) {
  NetMatrix <- biblioNetwork(M, analysis = "co-occurrences", network = "keywords", sep = ";")
  if (length(NetMatrix) > 0) {
    png(file.path(outdir, "rede_coocorrencia_palavras_chave.png"), width = 1400, height = 1200, res = 150)
    networkPlot(NetMatrix, normalize = "association", n = min(50, nrow(NetMatrix)),
                type = "fruchterman", size = TRUE, labelsize = 0.7, Title = "Coocorrência de palavras-chave")
    dev.off()
  }
}
writeLines(capture.output(sessionInfo()), file.path(outdir, "sessionInfo_R.txt"))
message("Concluído. Resultados em: ", outdir)
