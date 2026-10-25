# Relatório atualizado de validação municipal e harmonização — P2 Finanças do Setor Público (UnB)

Data da revisão: 25/10/2026. Municípios: Castanhal/PA (IBGE 1502400) e Abaetetuba/PA (IBGE 1500107). Período: 2015–2024.

## 1. O que foi efetivamente conferido

- O ZIP consolidado foi aberto e os arquivos-base lidos. A tabela detalhada `FINBRA_REGISTROS_MUNICIPIOS_2015_2024.csv` contém linhas municipais por ano, tipo de demonstrativo, rubrica, conta, valor e nome do arquivo de origem.
- A reconciliação interna foi refeita para 20 pares município-ano: receita bruta, deduções identificadas, despesa empenhada e população incorporada à exportação. A população da exportação de receita coincide com a população da exportação de despesa em 20/20 pares.
- Os valores totais financeiros da base consolidada foram preservados; as métricas per capita foram recalculadas usando, de modo uniforme, a população indicada nos próprios arquivos FINBRA/SICONFI. Isso elimina a mistura entre duas séries populacionais dentro dos indicadores recalculados, mas não certifica que a população FINBRA seja a melhor série demográfica anual para toda comparação.
- A documentação pública do SICONFI confirma a existência da consulta FINBRA/Contas Anuais e da API oficial DCA, e a consulta FINBRA exibe campo de período de homologação/retificação. Fontes oficiais: https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_finbra/finbra_list.jsf ; https://apidatalake.tesouro.gov.br/docs/siconfi/ .

## 2. O que NÃO foi certificado

- Não foi obtida nesta rodada uma resposta oficial linha a linha da última declaração DCA retificada de cada ente para os dez exercícios. Portanto, não se afirma que os números das exportações recebidas sejam a última versão homologada/retificada. A checagem do portal e da API foi confirmada no nível da documentação/consulta disponível, não no nível da última versão de cada observação.
- A população incorporada ao FINBRA foi harmonizada para cálculo reproduzível, mas não foi certificada como a série anual definitiva do IBGE. A página oficial do IBGE distingue população censitária de estimativa anual e recomenda observar a referência temporal e a base territorial. Para análises per capita finais, recomenda-se uma série anual única do IBGE, documentada ano a ano, caso seja possível obter e arquivar a tabela original. Com o denominador FINBRA usado nesta versão, a despesa real por habitante vai de R$ 2.621 a R$ 3.754 em Castanhal (+43,2%) e de R$ 2.308 a R$ 3.727 em Abaetetuba (+61,5%); estes resultados são condicionais, não uma certificação demográfica ou fiscal final.
- A variável `receita_bruta_menos_deducoes_identificadas` é calculada a partir das deduções que puderam ser identificadas no leiaute. Como cobertura e rubricas variam por ano, ela não deve ser chamada de “receita líquida oficial” sem reconciliação integral das deduções da DCA.

## 3. Status por observação

O arquivo `AUDITORIA_SICONFI_MUNICIPIOS_2015_2024.csv` contém 20 linhas, nome do arquivo de origem de receita e despesa, população, totais, contagens de linhas agregadas encontradas e um status separado para a checagem oficial de retificações. A checagem interna contra a exportação recebida não é equivalente à confirmação da última versão oficial.

## 4. Série populacional usada nos indicadores atualizados

Para eliminar a divergência interna, os novos campos `*_harmonizada*` usam a população da coluna `population` da exportação FINBRA de receita; foi verificado que ela coincide com a população da exportação de despesa em todos os 20 pares. Os campos originais baseados na série populacional anterior foram preservados como colunas históricas quando existentes. A mudança metodológica está documentada no CSV e no artigo.

## 5. Bibliografia: 80 referências versus 80 registros Scopus

A matriz de referências discutidas e a exportação Scopus são dois conjuntos diferentes. A auditoria anterior encontrou somente 9–10 coincidências exatas por DOI (a contagem varia conforme normalização/versão da matriz); não são conjuntos intercambiáveis. O arquivo de cruzamento foi mantido e o pacote agora registra essa divergência explicitamente. Não seria metodologicamente correto declarar a bibliometria como calculada sobre os 80 artigos do referencial.

A correção definitiva exige reexportar no Scopus os mesmos 80 artigos que permanecerão no texto, com metadados completos, e reexecutar Bibliometrix/Biblioshiny sobre essa exportação alinhada. Até isso ocorrer, os indicadores de 80 documentos descrevem somente a exportação Scopus atualmente disponível, não o conjunto dos 80 títulos do referencial. Também não há comprovação de leitura integral dos 80 textos; a matriz marca esse limite.

## 6. Conclusão operacional

**Validado internamente:** estrutura de 20 pares município-ano, arquivos de origem registrados, totais da base reconciliados com o consolidado recebido, igualdade da população entre exportações de receita e despesa, e recálculo per capita com denominador único.

**Ainda pendente de validação externa:** última versão/retificação DCA/SICONFI por município-ano, série anual demográfica oficial do IBGE, definição completa de deduções para receita líquida e alinhamento de corpus bibliográfico entre texto e bibliometria. Nenhum desses pontos é apresentado como concluído.
