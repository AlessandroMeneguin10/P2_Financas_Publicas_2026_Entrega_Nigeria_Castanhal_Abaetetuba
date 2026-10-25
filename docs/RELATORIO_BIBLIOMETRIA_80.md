# Bibliometria da exportação Scopus de 80 registros — relatório de execução e auditoria

## Escopo e procedimento
O corpus bibliométrico é a exportação Scopus de 80 registros usada pelo pesquisador no Bibliometrix/Biblioshiny (pacote `bibliometrix` 5.5.0, R 4.6.1, conforme registro do trabalho). Este relatório descreve apenas essa exportação; não afirma que ela seja idêntica à matriz dos 80 registros candidatos discutidos no referencial teórico.

## Indicadores reportados pelo Biblioshiny
- Período de publicação: 1978–2024
- Documentos: 80
- Fontes: 47
- Autores: 139
- Documentos de autoria única: 24
- Coautoria internacional: 21,25%
- Coautores por documento: 1,9
- Palavras-chave de autor: 135 (presentes em 43 dos 80 registros)
- Referências citadas: 2.827
- Idade média do documento: 19,1 anos
- Média de citações por documento: 64,24

Fontes mais frequentes reportadas: Public Choice (10), Journal of Public Economics (8), Publius: The Journal of Federalism (5), International Tax and Public Finance (3), Journal of Urban Economics (3), Public Budgeting and Finance (3), World Development (3), Estudos Econômicos (2), European Journal of Political Economy (2) e National Tax Journal (2). Palavras-chave frequentes: “flypaper effect” (13), “intergovernmental transfers” (11), “fiscal federalism” (8) e “fiscal illusion” (7).

## Reconciliação entre os dois conjuntos de 80
A matriz de referências candidatas e a exportação Scopus são diferentes. Após normalização de DOI, a matriz contém 80 linhas candidatas e foram encontradas 10 correspondências exatas com os DOIs disponíveis na exportação Scopus. Portanto, a bibliometria atual descreve a exportação Scopus auxiliar e não pode ser apresentada como bibliometria exata dos mesmos 80 artigos discutidos no texto. O arquivo `CRUZAMENTO_REFERENCIAL_vs_CORPUS_SCOPUS_80.csv` documenta o cruzamento.

A correção metodológica definitiva é construir uma lista final de 80 artigos que permaneçam no texto, reexportar exatamente esses registros no Scopus (ou documentar limitações de cobertura), e reexecutar Bibliometrix/Biblioshiny com a nova exportação. Não se deve simplesmente inferir que a amostra é a mesma porque ambas contêm 80 registros.

## Limitações
- O erro do gráfico “Most Relevant Authors” e o gráfico em branco “Authors’ Production over Time” relatados pelo pesquisador não são substituídos por estimativas inventadas.
- A leitura integral dos 80 artigos do referencial não está comprovada. Identidade bibliográfica, DOI e resumo não demonstram leitura integral ou elegibilidade acadêmica.
- Os indicadores da exportação dependem dos metadados presentes e descrevem somente o corpus Scopus importado.
