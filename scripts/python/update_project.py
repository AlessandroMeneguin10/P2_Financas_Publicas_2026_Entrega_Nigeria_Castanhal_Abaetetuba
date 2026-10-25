import os, json, zipfile, hashlib, re, math
import pandas as pd
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_BREAK

root='/mnt/data/p2work_update/ENTREGA_P2_242026481_BIBLIOMETRIA_FINAL'
# Load base
base=pd.read_csv(root+'/BASE_MUNICIPAL_RECONCILIADA_FINBRA_2015_2024.csv')
ana=pd.read_csv(root+'/BASE_MUNICIPAL_ANALITICA_REAL_2024.csv')
# One denominator series: population embedded in the same FINBRA export used for both revenue/expense
base['populacao_harmonizada_finbra'] = base['populacao_finbra_receita']
base['populacao_fonte_harmonizada'] = 'População reportada no mesmo arquivo FINBRA/SICONFI da receita; igual à coluna do arquivo de despesa nas 20 observações'
base['receita_bruta_menos_deducoes_identificadas'] = base['receita_bruta'] - base['deducoes_total']
base['receita_liquida_calculada'] = base['receita_bruta_menos_deducoes_identificadas'] # preserve old field but definition explicitly qualified
base['receita_liquida_per_capita'] = base['receita_bruta_menos_deducoes_identificadas'] / base['populacao_harmonizada_finbra']
base['despesa_empenhada_per_capita'] = base['despesa_empenhada'] / base['populacao_harmonizada_finbra']
base['status_validacao'] = 'Conferido internamente contra linha agregada da exportação recebida; retificação oficial não verificada'
base.to_csv(root+'/BASE_MUNICIPAL_RECONCILIADA_FINBRA_2015_2024.csv',index=False,encoding='utf-8-sig')
# Harmonized analytical base using same denominator for nominal and real per capita
ana['populacao_harmonizada_finbra'] = ana['populacao_finbra_receita']
ana['fonte_populacao_harmonizada'] = 'FINBRA/SICONFI: coluna population do arquivo de receita; conferida igual à coluna de despesa para 20/20 pares município-ano'
ana['receita_bruta_menos_deducoes_identificadas'] = ana['receita_bruta'] - ana['deducoes_total']
ana['receita_liquida_calculada'] = ana['receita_bruta_menos_deducoes_identificadas']
ana['receita_per_capita_nominal_harmonizada'] = ana['receita_bruta_menos_deducoes_identificadas']/ana['populacao_harmonizada_finbra']
ana['despesa_per_capita_nominal_harmonizada'] = ana['despesa_empenhada']/ana['populacao_harmonizada_finbra']
ana['receita_real_per_capita_harmonizada_2024'] = ana['receita_liquida_real_2024']/ana['populacao_harmonizada_finbra']
ana['despesa_real_per_capita_harmonizada_2024'] = ana['despesa_real_2024']/ana['populacao_harmonizada_finbra']
ana['status_validacao'] = 'Recalculado com denominador populacional único por observação; valores financeiros ainda aguardam reconciliação com última retificação DCA/SICONFI'
ana.to_csv(root+'/BASE_MUNICIPAL_ANALITICA_REAL_2024.csv',index=False,encoding='utf-8-sig')
# Build detailed audit from raw rows
raw=pd.read_csv(root+'/FINBRA_REGISTROS_MUNICIPIOS_2015_2024.csv',sep=';',encoding='utf-8-sig')
rows=[]
for _,r in base.sort_values(['municipio','ano']).iterrows():
    yr=int(r.ano); mun=r.municipio
    rawyr=raw[(raw.year==yr)&(raw.municipio==mun)]
    rev=rawyr[(rawyr.type=='receita') & (rawyr.col.str.contains('Receitas Brutas Realizadas|Total Receitas',case=False,na=False))]
    ded=rawyr[(rawyr.type=='receita') & (rawyr.col.str.contains('Deduções',case=False,na=False))]
    exp=rawyr[(rawyr.type=='despesa') & (rawyr.col.str.contains('Despesas Empenhadas',case=False,na=False)) & (rawyr.account.str.contains('Exceto Intraorçamentárias|Total Despesas',case=False,na=False))]
    rows.append({
      'ano':yr,'municipio':mun,'codigo_ibge':int(r.codigo_ibge),
      'arquivo_receita':r.receita_arquivo,'arquivo_despesa':r.despesa_arquivo,
      'populacao_finbra_receita':int(r.populacao_finbra_receita),'populacao_finbra_despesa':int(r.populacao_finbra_despesa),
      'populacao_igual_entre_arquivos':bool(r.populacao_finbra_receita==r.populacao_finbra_despesa),
      'receita_bruta':float(r.receita_bruta),'deducoes_identificadas':float(r.deducoes_total),
      'receita_bruta_menos_deducoes_identificadas':float(r.receita_bruta-r.deducoes_total),
      'despesa_empenhada':float(r.despesa_empenhada),
      'linhas_receita_total_encontradas_no_recorte':len(rev),'linhas_deducao_encontradas_no_recorte':len(ded),'linhas_despesa_total_encontradas_no_recorte':len(exp),
      'checagem_interna_csv':'PASSOU' if (len(rev)>=1 and len(exp)>=1 and r.populacao_finbra_receita==r.populacao_finbra_despesa) else 'REVISAR',
      'portal_oficial_ultima_retificacao':'NÃO VERIFICADO nesta rodada',
      'fonte_oficial_consulta':'https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_finbra/finbra_list.jsf',
      'api_oficial_documentacao':'https://apidatalake.tesouro.gov.br/docs/siconfi/',
      'observacao':'Exportação FINBRA recebida; conferir versão/competência de homologação-retificação. Deduções identificadas variam por leiaute; não chamar resultado de receita líquida oficial sem reconciliação completa.'
    })
audit=pd.DataFrame(rows).sort_values(['ano','municipio'])
audit.to_csv(root+'/AUDITORIA_SICONFI_MUNICIPIOS_2015_2024.csv',index=False,encoding='utf-8-sig')
# New validation report
report='''# Relatório atualizado de validação municipal e harmonização — P2 Finanças do Setor Público (UnB)\n\nData da revisão: 25/10/2026. Municípios: Castanhal/PA (IBGE 1502400) e Abaetetuba/PA (IBGE 1500107). Período: 2015–2024.\n\n## 1. O que foi efetivamente conferido\n\n- O ZIP consolidado foi aberto e os arquivos-base lidos. A tabela detalhada `FINBRA_REGISTROS_MUNICIPIOS_2015_2024.csv` contém linhas municipais por ano, tipo de demonstrativo, rubrica, conta, valor e nome do arquivo de origem.\n- A reconciliação interna foi refeita para 20 pares município-ano: receita bruta, deduções identificadas, despesa empenhada e população incorporada à exportação. A população da exportação de receita coincide com a população da exportação de despesa em 20/20 pares.\n- Os valores totais financeiros da base consolidada foram preservados; as métricas per capita foram recalculadas usando, de modo uniforme, a população indicada nos próprios arquivos FINBRA/SICONFI. Isso elimina a mistura entre duas séries populacionais dentro dos indicadores recalculados, mas não certifica que a população FINBRA seja a melhor série demográfica anual para toda comparação.\n- A documentação pública do SICONFI confirma a existência da consulta FINBRA/Contas Anuais e da API oficial DCA, e a consulta FINBRA exibe campo de período de homologação/retificação. Fontes oficiais: https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_finbra/finbra_list.jsf ; https://apidatalake.tesouro.gov.br/docs/siconfi/ .\n\n## 2. O que NÃO foi certificado\n\n- Não foi obtida nesta rodada uma resposta oficial linha a linha da última declaração DCA retificada de cada ente para os dez exercícios. Portanto, não se afirma que os números das exportações recebidas sejam a última versão homologada/retificada. A checagem do portal e da API foi confirmada no nível da documentação/consulta disponível, não no nível da última versão de cada observação.\n- A população incorporada ao FINBRA foi harmonizada para cálculo reproduzível, mas não foi certificada como a série anual definitiva do IBGE. A página oficial do IBGE distingue população censitária de estimativa anual e recomenda observar a referência temporal e a base territorial. Para análises per capita finais, recomenda-se uma série anual única do IBGE, documentada ano a ano, caso seja possível obter e arquivar a tabela original.\n- A variável `receita_bruta_menos_deducoes_identificadas` é calculada a partir das deduções que puderam ser identificadas no leiaute. Como cobertura e rubricas variam por ano, ela não deve ser chamada de “receita líquida oficial” sem reconciliação integral das deduções da DCA.\n\n## 3. Status por observação\n\nO arquivo `AUDITORIA_SICONFI_MUNICIPIOS_2015_2024.csv` contém 20 linhas, nome do arquivo de origem de receita e despesa, população, totais, contagens de linhas agregadas encontradas e um status separado para a checagem oficial de retificações. A checagem interna contra a exportação recebida não é equivalente à confirmação da última versão oficial.\n\n## 4. Série populacional usada nos indicadores atualizados\n\nPara eliminar a divergência interna, os novos campos `*_harmonizada*` usam a população da coluna `population` da exportação FINBRA de receita; foi verificado que ela coincide com a população da exportação de despesa em todos os 20 pares. Os campos originais baseados na série populacional anterior foram preservados como colunas históricas quando existentes. A mudança metodológica está documentada no CSV e no artigo.\n\n## 5. Bibliografia: 80 referências versus 80 registros Scopus\n\nA matriz de referências discutidas e a exportação Scopus são dois conjuntos diferentes. A auditoria anterior encontrou somente 9–10 coincidências exatas por DOI (a contagem varia conforme normalização/versão da matriz); não são conjuntos intercambiáveis. O arquivo de cruzamento foi mantido e o pacote agora registra essa divergência explicitamente. Não seria metodologicamente correto declarar a bibliometria como calculada sobre os 80 artigos do referencial.\n\nA correção definitiva exige reexportar no Scopus os mesmos 80 artigos que permanecerão no texto, com metadados completos, e reexecutar Bibliometrix/Biblioshiny sobre essa exportação alinhada. Até isso ocorrer, os indicadores de 80 documentos descrevem somente a exportação Scopus atualmente disponível, não o conjunto dos 80 títulos do referencial. Também não há comprovação de leitura integral dos 80 textos; a matriz marca esse limite.\n\n## 6. Conclusão operacional\n\n**Validado internamente:** estrutura de 20 pares município-ano, arquivos de origem registrados, totais da base reconciliados com o consolidado recebido, igualdade da população entre exportações de receita e despesa, e recálculo per capita com denominador único.\n\n**Ainda pendente de validação externa:** última versão/retificação DCA/SICONFI por município-ano, série anual demográfica oficial do IBGE, definição completa de deduções para receita líquida e alinhamento de corpus bibliográfico entre texto e bibliometria. Nenhum desses pontos é apresentado como concluído.\n'''
open(root+'/RELATORIO_CONSOLIDACAO_E_LIMITACOES.md','w',encoding='utf-8').write(report)
open(root+'/RELATORIO_PENDENCIAS_FINAIS_AUDITORIA.md','w',encoding='utf-8').write('''# Pendências finais — status atualizado\n\n## Feito nesta atualização\n- Abri e inspecionei o ZIP consolidado e li a continuidade do projeto.\n- Reorganizei a auditoria municipal em 20 observações município-ano, incluindo nomes dos arquivos de receita/despesa, população FINBRA, totais, contagens de linhas agregadas e status específico da retificação oficial.\n- Confirmei internamente que a população nas exportações de receita e despesa coincide em 20/20 pares. Recalculei os indicadores per capita usando uma única série populacional (população embutida no FINBRA recebido).\n- Atualizei o relatório e o artigo para deixar explícita a diferença entre conferência interna da exportação e validação da última declaração oficial.\n- Mantive explícita a divergência entre os 80 registros Scopus e a matriz de 80 referências; não os declarei como o mesmo corpus.\n\n## Pendências abertas, sem alegar conclusão\n1. Obter/arquivar a versão oficial mais recente da DCA para cada ente e exercício e verificar o período de homologação/retificação.\n2. Substituir ou validar a população FINBRA por uma única série anual oficial do IBGE, com arquivos-fonte por ano.\n3. Conferir as rubricas de deduções em cada leiaute antes de rotular a variável como receita líquida oficial.\n4. Reexportar no Scopus os mesmos 80 artigos efetivamente mantidos no texto e reexecutar Bibliometrix/Biblioshiny sobre esse corpus alinhado.\n5. Comprovar leitura e elegibilidade dos 80 artigos; metadados editoriais não comprovam leitura integral.\n\n## Fontes oficiais consultadas\n- SICONFI — consulta FINBRA/Contas Anuais: https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_finbra/finbra_list.jsf\n- Tesouro Nacional — documentação da API SICONFI (inclui DCA e extrato de entregas): https://apidatalake.tesouro.gov.br/docs/siconfi/\n- IBGE — estimativas de população: https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html\n- IBGE — Castanhal: https://www.ibge.gov.br/cidades-e-estados/pa/castanhal.html\n- IBGE — Abaetetuba: https://www.ibge.gov.br/cidades-e-estados/pa/abaetetuba.html\n''')
# Population chart recomputed on unified FINBRA population series
ana=ana.sort_values(['municipio','ano'])
plt.figure(figsize=(8.5,5.2))
for mun,g in ana.groupby('municipio'):
    plt.plot(g['ano'],g['despesa_real_2024']/g['populacao_harmonizada_finbra'],marker='o',label=mun)
plt.title('Despesa empenhada por habitante (R$ de 2024)')
plt.xlabel('Ano'); plt.ylabel('R$ por habitante'); plt.xticks(range(2015,2025),rotation=45); plt.legend(); plt.tight_layout()
plt.savefig(root+'/despesa_per_capita_real_2024.png',dpi=180); plt.close()
plt.figure(figsize=(8.5,5.2))
for mun,g in ana.groupby('municipio'):
    plt.plot(g['ano'],g['receita_liquida_real_2024']/g['populacao_harmonizada_finbra'],marker='o',label=mun)
plt.title('Receita bruta menos deduções identificadas por habitante (R$ de 2024)')
plt.xlabel('Ano'); plt.ylabel('R$ por habitante'); plt.xticks(range(2015,2025),rotation=45); plt.legend(); plt.tight_layout()
plt.savefig(root+'/receita_despesa_real_2024.png',dpi=180); plt.close()
# Bibliographic crosswalk recalculation
mat=pd.read_csv(root+'/MATRIZ_AUDITORIA_FINAL_80_REFERENCIAS.csv',encoding='utf-8-sig')
sc=pd.read_csv(root+'/BASE_80_COM_METADADOS_SCOPUS.csv',encoding='utf-8-sig')
def normdoi(x):
    if pd.isna(x): return ''
    x=str(x).strip().lower()
    x=re.sub(r'^https?://(dx\.)?doi\.org/','',x)
    x=x.replace('doi:','').strip().rstrip('.,;')
    return x
mat['doi_norm_recalc']=mat['doi'].map(normdoi)
sc['doi_norm_recalc']=sc['DOI'].map(normdoi)
sc_dois=set(x for x in sc['doi_norm_recalc'] if x)
mat['match_doi_exact_recalculado']=mat['doi_norm_recalc'].apply(lambda x: bool(x and x in sc_dois))
# title similarity with rapidfuzz if available
try:
 from rapidfuzz import fuzz,process
 def normtitle(x): return re.sub(r'[^a-z0-9]+',' ',str(x).lower()).strip()
 titles=[normtitle(x) for x in sc['Title'].fillna('')]
 def best(t):
  t=normtitle(t)
  if not t: return ('',0)
  bestv=max(((str(sc.iloc[i]['Title']),fuzz.ratio(t,tt)) for i,tt in enumerate(titles)),key=lambda z:z[1],default=('',0))
  return bestv
 mat[['melhor_titulo_scopus_recalculado','similaridade_titulo_recalculada_pct']]=mat['titulo'].apply(lambda x: pd.Series(best(x)))
except Exception:
 mat['melhor_titulo_scopus_recalculado']=''
 mat['similaridade_titulo_recalculada_pct']=pd.NA
mat.to_csv(root+'/MATRIZ_AUDITORIA_FINAL_80_REFERENCIAS.csv',index=False,encoding='utf-8-sig')
# Update crosswalk with recalculated DOI flag and title similarity
cross=pd.read_csv(root+'/CRUZAMENTO_REFERENCIAL_vs_CORPUS_SCOPUS_80.csv',encoding='utf-8-sig')
if 'n_referencial' in cross.columns:
    x=mat[['id_original','titulo','doi','match_doi_exact_recalculado','melhor_titulo_scopus_recalculado','similaridade_titulo_recalculada_pct']].copy()
    x=x.rename(columns={'id_original':'n_referencial','titulo':'titulo_referencial','doi':'doi_referencial','match_doi_exact_recalculado':'correspondencia_doi_exata_recalculada','melhor_titulo_scopus_recalculado':'melhor_titulo_scopus_recalculado','similaridade_titulo_recalculada_pct':'similaridade_titulo_recalculada_pct'})
    x.to_csv(root+'/CRUZAMENTO_REFERENCIAL_vs_CORPUS_SCOPUS_80.csv',index=False,encoding='utf-8-sig')
# Update README
readme=root+'/README_PACOTE_FINAL.md'
with open(readme,'a',encoding='utf-8') as f:
 if '## Atualização de auditoria (25/10/2026)' not in open(readme,encoding='utf-8').read(): f.write('\n\n## Atualização de auditoria (25/10/2026)\n\nFoi refeita a conferência interna das 20 observações município-ano a partir das exportações FINBRA recebidas. Os indicadores per capita recalculados usam a população informada no arquivo FINBRA de receita, verificada igual à do arquivo de despesa em 20/20 pares. Isso harmoniza o denominador internamente, mas não certifica a população como série anual oficial definitiva do IBGE. A última retificação DCA/SICONFI não foi verificada linha a linha; consulte `RELATORIO_CONSOLIDACAO_E_LIMITACOES.md` e `AUDITORIA_SICONFI_MUNICIPIOS_2015_2024.csv`.\n\nA receita calculada é “receita bruta menos deduções identificadas”, não uma receita líquida oficial certificada, porque a cobertura de deduções varia por leiaute. A matriz dos 80 registros do referencial continua diferente da exportação Scopus de 80 registros; a bibliometria descreve apenas o corpus Scopus. A leitura integral dos 80 artigos não está comprovada.\n')
# Update article with truthful current notes and replace relevant paragraphs
pdoc=root+'/artigo_242026481_atualizado.docx'
doc=Document(pdoc)
replacements={
5: 'Nota de transparência: este manuscrito combina uma matriz de 80 referências candidatas, uma análise fiscal municipal exploratória e contexto macrofiscal da Nigéria. A leitura integral de todos os textos não está comprovada. Os totais foram conferidos internamente contra as exportações FINBRA/SICONFI recebidas para 20 pares município-ano; isso não comprova que sejam a última versão homologada/retificada da DCA. Nesta atualização, os indicadores per capita foram recalculados com a população embutida nas mesmas exportações FINBRA, que coincide entre os arquivos de receita e despesa em 20/20 pares. Essa harmonização interna não certifica a série demográfica anual como a série oficial definitiva do IBGE. A exportação Scopus usada no Bibliometrix contém 80 registros distintos da matriz do referencial; os indicadores bibliométricos descrevem somente a exportação Scopus.',
31: 'Nota de escopo bibliográfico: esta seção apresenta síntese temática de 80 registros candidatos distintos, usando metadados, resumos e páginas editoriais/institucionais quando disponíveis. A matriz registra separadamente o estado de verificação e de leitura. Como a leitura integral de todos os textos não está comprovada, o conjunto não deve ser descrito como 80 artigos integralmente lidos. A análise bibliométrica foi executada sobre uma exportação Scopus separada de 80 registros; o cruzamento por DOI/título não demonstra que sejam o mesmo corpus.',
129: 'A análise bibliométrica foi executada no Bibliometrix/Biblioshiny (pacote bibliometrix 5.5.0, em R 4.6.1) no computador do pesquisador, sobre a exportação Scopus de 80 registros. A conversão foi feita com convert2df (dbsource = “scopus”, formato CSV) e a análise descritiva com biblioAnalysis. O corpus é a amostra exportada para a análise, não o universo de toda a literatura sobre federalismo fiscal e não é idêntico à matriz de 80 referências discutidas no referencial. O cruzamento de DOI e títulos mostra que as amostras não podem ser tratadas como intercambiáveis; para alinhar as exigências, será necessário reexportar no Scopus os mesmos artigos que permanecerem no texto e reexecutar a análise.',
139: 'A leitura dos CSVs FINBRA recebidos encontrou linhas totais de despesa empenhada para os dois municípios em todos os anos de 2015–2024. A receita bruta foi extraída dos totais apresentados e a variável derivada foi calculada subtraindo apenas as deduções identificadas no leiaute de cada ano. Como a cobertura e a classificação das deduções variam entre arquivos, essa variável deve ser denominada “receita bruta menos deduções identificadas”, não receita líquida oficial certificada. Os arquivos de origem estão registrados na base de auditoria. A consulta FINBRA e a documentação da API oficial foram localizadas, mas não foi possível confirmar linha a linha a última versão retificada de cada declaração DCA para os 20 pares município-ano.',
143: 'O deflacionamento é aplicado aos agregados monetários antes do cálculo por habitante. Nesta atualização, para eliminar a mistura de denominadores, os indicadores per capita foram recalculados com a população informada na exportação FINBRA de receita; ela coincide com a população da exportação de despesa nos 20 pares município-ano. Essa é uma harmonização operacional da base recebida, não uma certificação de que a população FINBRA seja a série anual oficial definitiva do IBGE. A validação demográfica final requer arquivar e conferir uma série anual única do IBGE.',
152: 'Com os totais de despesa empenhada extraídos dos CSVs FINBRA, o IPCA anual e a população indicada nos mesmos arquivos FINBRA, a despesa por habitante em reais de 2024 foi recalculada com um denominador uniforme dentro de cada município-ano. Os valores de referência e percentuais de variação devem ser lidos na base analítica atualizada. Eles permanecem preliminares quanto à versão retificada da DCA/SICONFI e à escolha definitiva da série demográfica anual; não demonstram efeitos causais.',
163: 'As limitações são substantivas e estão documentadas: (i) os 20 pares município-ano foram conferidos internamente contra as exportações FINBRA recebidas, mas a última versão retificada da DCA/SICONFI não foi verificada linha a linha; (ii) os indicadores per capita foram harmonizados usando a população embutida nos mesmos arquivos FINBRA, mas essa série ainda não foi certificada como a série anual definitiva do IBGE; (iii) a variável de receita é receita bruta menos deduções identificadas e não receita líquida oficial certificada; (iv) a matriz bibliográfica de 80 referências não coincide com os 80 registros Scopus usados na bibliometria; (v) a leitura integral dos 80 textos não está comprovada. Os resultados devem ser interpretados como exploratórios.'
}
for i,txt in replacements.items():
 if i < len(doc.paragraphs): doc.paragraphs[i].text=txt
# Insert explicit short section near final status paragraph by appending before references end (appendix-like transparent audit note)
p=doc.add_paragraph()
p.style='Normal'
p.add_run('Atualização de auditoria e limites de validação (25/10/2026)')
for txt in [
 'Conferência interna: foram identificados os totais de receita bruta, deduções disponíveis, despesa empenhada e população nos arquivos FINBRA recebidos para 20 combinações de município e ano. A população presente na exportação de receita coincide com a da exportação de despesa em 20 de 20 combinações. Os indicadores per capita desta versão usam essa série única para evitar misturar denominadores.',
 'Validação externa pendente: a página oficial do SICONFI permite consultar Contas Anuais/FINBRA e apresenta período de homologação/retificação; a API oficial documenta o acesso a DCA e extrato de entregas. Porém, nesta revisão não foi obtida evidência individual de que cada número corresponda à última declaração retificada. Por isso, a validação oficial final não é declarada concluída.',
 'A variável de receita é receita bruta menos deduções identificadas nos layouts recebidos. Como as deduções variam por ano, não equivale necessariamente à receita líquida oficial integral. A matriz de 80 referências e a exportação Scopus de 80 documentos são corpora diferentes; a bibliometria não pode ser atribuída à lista discutida até que a exportação seja alinhada e a análise seja reexecutada.',
 'Fontes oficiais de consulta: SICONFI FINBRA (https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_finbra/finbra_list.jsf); documentação da API SICONFI (https://apidatalake.tesouro.gov.br/docs/siconfi/); IBGE Estimativas da População (https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html).'
]: doc.add_paragraph(txt)
doc.save(pdoc)
# Generate a text summary of recomputed values
summary=[]
for mun,g in ana.groupby('municipio'):
 g=g.sort_values('ano'); a=g.iloc[0]; z=g.iloc[-1]
 start=float(a['despesa_real_2024']/a['populacao_harmonizada_finbra']); end=float(z['despesa_real_2024']/z['populacao_harmonizada_finbra'])
 summary.append({'municipio':mun,'pop_2015':int(a['populacao_harmonizada_finbra']),'pop_2024':int(z['populacao_harmonizada_finbra']),'despesa_real_pc_2015':start,'despesa_real_pc_2024':end,'variacao_pct':(end/start-1)*100})
with open(root+'/RESUMO_AUDITORIA_80.json','r',encoding='utf-8') as f: old=json.load(f)
old['atualizacao_2026_10_25']={'municipal_rows_internal_checked':20,'population_equal_between_revenue_and_expense_exports':20,'official_last_rectification_verified':False,'population_harmonization':'FINBRA population field from revenue export, same as expense export for 20/20 pairs','scopus_corpus_equals_80_reference_matrix':False,'full_text_reading_of_80_confirmed':False,'despesa_real_pc_summary':summary}
with open(root+'/RESUMO_AUDITORIA_80.json','w',encoding='utf-8') as f: json.dump(old,f,ensure_ascii=False,indent=2)
print('DONE')
print('summaries',summary)
print('mat DOI exact',int(mat['match_doi_exact_recalculado'].sum()),'of',len(mat),'Scopus DOI unique',len(sc_dois))
