# Relatório de conferência FINBRA/SICONFI — Castanhal e Abaetetuba

Data: 25/10/2026

## Escopo
Foram examinadas as exportações FINBRA/SICONFI recebidas e o pacote consolidado. A base detalhada registra exercício, município, código IBGE, população, tipo de demonstrativo, rubrica/conta, valor e nome do arquivo de origem.

## Resultado da conferência interna
- Foram localizados os totais financeiros para 20 pares município-ano (Castanhal e Abaetetuba, 2015–2024) nas exportações que compõem o pacote.
- A população informada nos arquivos de receita e despesa coincide em 20/20 pares. Os indicadores per capita foram recalculados usando a população do arquivo FINBRA de receita como denominador único por observação.
- A receita derivada foi renomeada conceitualmente para “receita bruta menos deduções identificadas”. Não se deve chamá-la de receita líquida oficial, pois a cobertura das deduções varia por leiaute e não foi possível certificar a captura integral de todas as rubricas.
- Os totais são conferidos internamente contra as exportações recebidas, mas isso não certifica que representem a última declaração DCA homologada/retificada.

## Conferência externa e retificações
A consulta pública oficial FINBRA/Contas Anuais e a documentação da API SICONFI foram localizadas. A consulta oficial indica a possibilidade de pesquisar período de homologação/retificação, e a API documenta endpoints de DCA e extrato de entregas. Nesta rodada, porém, não foi recuperada evidência individual por município-ano que confirme a última versão retificada para todos os 20 pares. Portanto, a validação externa final continua pendente.

## População
A população FINBRA foi usada como série harmonizada operacional, pois a coluna coincide entre os arquivos de receita e despesa. Isso resolve a inconsistência interna dos denominadores, mas não certifica que os valores sejam a série anual definitiva de estimativas do IBGE. Para uma validação demográfica final, deve-se arquivar uma tabela anual única do IBGE com referência temporal explícita.

## Fontes oficiais
- SICONFI — consulta FINBRA/Contas Anuais: https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_finbra/finbra_list.jsf
- API SICONFI — documentação: https://apidatalake.tesouro.gov.br/docs/siconfi/
- IBGE — estimativas da população: https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html

**Status final:** conferência interna das exportações concluída; última retificação DCA/SICONFI e série demográfica anual definitiva do IBGE não certificadas.
