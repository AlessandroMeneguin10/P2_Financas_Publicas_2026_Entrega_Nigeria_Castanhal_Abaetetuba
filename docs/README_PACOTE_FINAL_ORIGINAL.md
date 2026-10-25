# P2 Finanças do Setor Público — pacote consolidado de trabalho

Este pacote reúne a versão atualizada do artigo, a seção bibliométrica, tabelas de apoio, o corpus Scopus selecionado e uma reconstrução da série municipal com os CSVs FINBRA fornecidos.

## Arquivos principais
- `artigo_242026481_atualizado.docx` e `pdf/artigo_242026481_atualizado.pdf`: artigo com seção bibliométrica e valores municipais atualizados.
- `BASE_MUNICIPAL_RECONCILIADA_FINBRA_2015_2024.csv`: totais de receita/deduções/despesa por município-ano, com arquivo de origem.
- `BASE_MUNICIPAL_ANALITICA_REAL_2024.csv`: base com valores deflacionados pelo IPCA até preços de 2024 e indicadores por habitante.
- `PRODUCAO_ANUAL_80.csv`, `PERIODICOS_80.csv`, `AUTORES_80.csv`, `PALAVRAS_CHAVE_80.csv`: tabelas descritivas da amostra Scopus de 80 registros.
- `AUTORES_RELEVANTES_RESULTADO_R.csv`: top autores extraídos pelo usuário no R/Bibliometrix.
- `CRUZAMENTO_REFERENCIAL_vs_CORPUS_SCOPUS_80.csv`: comparação entre a matriz de referências discutidas e o corpus Scopus usado na análise.
- `dados_brutos_finbra/`: CSVs FINBRA originais que foram encontrados no material de trabalho.

## Limitações que não devem ser ocultadas
A amostra bibliométrica Scopus de 80 registros não é idêntica à matriz de 80 referências do artigo; o cruzamento por DOI normalizado encontrou 10 correspondências exatas. A bibliometria caracteriza somente o corpus Scopus auxiliar. A matriz de referências mantém status de verificação e não comprova leitura integral de todos os textos. Na série municipal, os totais foram conferidos internamente para 20 observações. A receita é apresentada como receita bruta menos deduções identificadas, porque a cobertura dessas categorias varia. Não foi confirmada a última retificação DCA/SICONFI por observação. Os indicadores per capita usam a população FINBRA harmonizada entre arquivos de receita e despesa, mas isso não certifica a série anual definitiva do IBGE.

## Reprodução
Os CSVs de tabelas e os scripts/relatórios de apoio estão incluídos. O deflacionamento usa as taxas anuais do IPCA de 2016 a 2024 para converter os valores nominais de cada ano a reais de 2024. A base não imputa ausências a zero.


## Auditoria final de consistência (25/10/2026)
Consulte `RELATORIO_PENDENCIAS_FINAIS_AUDITORIA.md` e `MATRIZ_AUDITORIA_FINAL_80_REFERENCIAS.csv`. A comparação por DOI encontrou somente dez correspondências entre a matriz de referências discutidas e o corpus Scopus usado na bibliometria. Os conjuntos são mantidos separados e isso é explicitado no artigo. A leitura integral dos 80 textos não está comprovada. A série municipal está deflacionada para reais de 2024 e usa denominador populacional harmonizado internamente; a validação da série anual oficial do IBGE e a conferência de retificações DCA/SICONFI continuam pendentes.


## Atualização de auditoria (25/10/2026)

Foi refeita a conferência interna das 20 observações município-ano a partir das exportações FINBRA recebidas. Os indicadores per capita recalculados usam a população informada no arquivo FINBRA de receita, verificada igual à do arquivo de despesa em 20/20 pares. Isso harmoniza o denominador internamente, mas não certifica a população como série anual oficial definitiva do IBGE. A última retificação DCA/SICONFI não foi verificada linha a linha; consulte `RELATORIO_CONSOLIDACAO_E_LIMITACOES.md` e `AUDITORIA_SICONFI_MUNICIPIOS_2015_2024.csv`.

A receita calculada é “receita bruta menos deduções identificadas”, não uma receita líquida oficial certificada, porque a cobertura de deduções varia por leiaute. A matriz dos 80 registros do referencial continua diferente da exportação Scopus de 80 registros; a bibliometria descreve apenas o corpus Scopus. A leitura integral dos 80 artigos não está comprovada.


## Códigos de reprodução Python e R
Consulte `codigo_reproducao/README_CODIGOS.md`. Foram incluídos scripts para inventário de arquivos, validação estrutural, resumo bibliométrico, gráficos exploratórios e análise Bibliometrix em R. Os scripts precisam ser executados e conferidos no ambiente local; a inclusão não implica execução bem-sucedida.
