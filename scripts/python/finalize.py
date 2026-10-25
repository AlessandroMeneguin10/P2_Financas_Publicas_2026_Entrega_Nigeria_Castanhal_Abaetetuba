import os,zipfile,shutil,hashlib,json
import pandas as pd
from docx import Document
root='/mnt/data/p2work_update/ENTREGA_P2_242026481_BIBLIOMETRIA_FINAL'
# corrected concise municipal base from reconciled data
b=pd.read_csv(root+'/BASE_MUNICIPAL_RECONCILIADA_FINBRA_2015_2024.csv')
a=pd.read_csv(root+'/BASE_MUNICIPAL_ANALITICA_REAL_2024.csv')
rows=[]
for _,r in a.iterrows():
 pop=int(r['populacao_harmonizada_finbra'])
 rows.append({'ano':int(r.ano),'municipio':r.municipio,'codigo_ibge':int(r.codigo_ibge),'populacao_finbra_harmonizada':pop,'receita_bruta':r.receita_bruta,'deducoes_identificadas':r.deducoes_total,'receita_bruta_menos_deducoes_identificadas':r.receita_bruta-r.deducoes_total,'despesa_empenhada':r.despesa_empenhada,'saldo_despesa_menos_receita_derivada':r.despesa_empenhada-(r.receita_bruta-r.deducoes_total),'receita_derivada_per_capita_nominal':(r.receita_bruta-r.deducoes_total)/pop,'despesa_empenhada_per_capita_nominal':r.despesa_empenhada/pop,'fator_ipca_para_reais_2024':r.fator_para_reais_2024,'receita_derivada_real_2024':r.receita_liquida_real_2024,'despesa_real_2024':r.despesa_real_2024,'receita_derivada_real_per_capita_2024':r.receita_liquida_real_2024/pop,'despesa_real_per_capita_2024':r.despesa_real_2024/pop,'status':'Exploratório; arquivo FINBRA recebido conferido internamente; retificação oficial e série IBGE ainda pendentes'})
pd.DataFrame(rows).to_csv(root+'/BASE_MUNICIPAL_CORRIGIDA_P2_2015_2024.csv',index=False,encoding='utf-8-sig')
# replace article remaining old claims
pdoc=root+'/artigo_242026481_atualizado.docx'; d=Document(pdoc)
repl={
151:'Figura 2. Despesa empenhada por habitante em reais de 2024, após atualização pelo IPCA. Fonte: arquivos FINBRA/SICONFI fornecidos; população embutida na exportação FINBRA, harmonizada entre receitas e despesas; IPCA anual; cálculos próprios. A população ainda não foi certificada como série anual definitiva do IBGE.',
154:'A diferença entre municípios varia ao longo do período. Em 2024, a despesa empenhada por habitante, em preços de 2024, foi de aproximadamente R$ 3.754 em Castanhal e R$ 3.727 em Abaetetuba, diferença de cerca de R$ 27, usando a população embutida nos arquivos FINBRA recebidos. Diferenças podem refletir estrutura econômica, composição demográfica, serviços prestados, transferências e práticas de registro, não apenas eficiência fiscal.',
159:'Os dados permitem descrever trajetórias de despesa empenhada por habitante em reais de 2024, calculadas a partir dos CSVs FINBRA/SICONFI fornecidos, do IPCA anual e da população indicada nos mesmos arquivos FINBRA. A população foi harmonizada internamente entre exportações de receita e despesa, mas não foi certificada como a série anual definitiva do IBGE; as declarações também não foram reconciliadas com as versões retificadas da DCA/SICONFI. Não permitem afirmar expansão real de serviços, melhora de eficiência, aumento causal decorrente de transferências ou presença do efeito flypaper.',
161:'Com o denominador populacional harmonizado à população indicada nos arquivos FINBRA recebidos, a despesa empenhada por habitante em reais de 2024 passou aproximadamente de R$ 2.621 para R$ 3.754 em Castanhal entre 2015 e 2024 (aumento de 43,2%) e de R$ 2.308 para R$ 3.727 em Abaetetuba (aumento de 61,5%). Esses percentuais são descritivos e permanecem condicionados à conferência da população em série oficial anual e à verificação das retificações DCA/SICONFI; não demonstram causalidade.',
257:'A matriz bibliográfica contém 80 registros candidatos distintos. A exportação Scopus contém outros 80 registros; o cruzamento DOI normalizado encontrou dez coincidências, de modo que os corpora não são idênticos. O texto integral dos 80 artigos do referencial não está comprovadamente lido. A análise Bibliometrix/Biblioshiny descreve apenas a exportação Scopus disponível. Os dados fiscais foram conferidos internamente contra os CSVs FINBRA recebidos, mas a última versão retificada da DCA/SICONFI não foi verificada linha a linha. Os indicadores per capita usam uma única população por observação extraída do FINBRA, sem certificar a série anual do IBGE. Não apresentar o manuscrito como empiricamente 100% validado sem resolver esses bloqueios.'
}
for i,t in repl.items(): d.paragraphs[i].text=t
d.save(pdoc)
# update report numeric examples
p=root+'/RELATORIO_CONSOLIDACAO_E_LIMITACOES.md'
s=open(p,encoding='utf-8').read()
s=s.replace('Para análises per capita finais, recomenda-se uma série anual única do IBGE, documentada ano a ano, caso seja possível obter e arquivar a tabela original.','Para análises per capita finais, recomenda-se uma série anual única do IBGE, documentada ano a ano, caso seja possível obter e arquivar a tabela original. Com o denominador FINBRA usado nesta versão, a despesa real por habitante vai de R$ 2.621 a R$ 3.754 em Castanhal (+43,2%) e de R$ 2.308 a R$ 3.727 em Abaetetuba (+61,5%); estes resultados são condicionais, não uma certificação demográfica ou fiscal final.')
open(p,'w',encoding='utf-8').write(s)
# Ensure PDF generated from current docx
pdfdir='/mnt/data/p2work_update/pdfbuild'; os.makedirs(pdfdir,exist_ok=True)
os.system("libreoffice --headless --convert-to pdf --outdir '{}' '{}' >/tmp/lo2.txt 2>&1".format(pdfdir,pdoc))
newpdf=pdfdir+'/artigo_242026481_atualizado.pdf'
if os.path.exists(newpdf):
 shutil.copy2(newpdf,root+'/artigo_242026481_atualizado.pdf')
 shutil.copy2(newpdf,root+'/pdf/artigo_242026481_atualizado.pdf')
# Rebuild ZIP with the package's top-level folder
out='/mnt/data/ENTREGA_P2_242026481_CONSOLIDADA_ATUALIZADA_2026-10-25.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for fn in sorted(os.listdir(root)):
  full=os.path.join(root,fn)
  if os.path.isfile(full): z.write(full,arcname='ENTREGA_P2_242026481_BIBLIOMETRIA_FINAL/'+fn)
  elif os.path.isdir(full):
   for dp,ds,fs in os.walk(full):
    for f in fs:
     path=os.path.join(dp,f); z.write(path,arcname='ENTREGA_P2_242026481_BIBLIOMETRIA_FINAL/'+os.path.relpath(path,root))
# verify ZIP and outputs
with zipfile.ZipFile(out) as z:
 bad=z.testzip(); names=z.namelist()
 assert bad is None, bad
 assert any(x.endswith('artigo_242026481_atualizado.pdf') for x in names)
 assert any(x.endswith('AUDITORIA_SICONFI_MUNICIPIOS_2015_2024.csv') for x in names)
 assert any(x.endswith('CRUZAMENTO_REFERENCIAL_vs_CORPUS_SCOPUS_80.csv') for x in names)
print('ZIP',out,os.path.getsize(out),'files',len(names),'testzip',bad)
print('PDF',os.path.getsize(root+'/artigo_242026481_atualizado.pdf'))
print('BASE_ROWS',len(a),'AUDIT_ROWS',len(pd.read_csv(root+'/AUDITORIA_SICONFI_MUNICIPIOS_2015_2024.csv')))
print('DOI_MATCHES',int(pd.read_csv(root+'/MATRIZ_AUDITORIA_FINAL_80_REFERENCIAS.csv')['match_doi_exact_recalculado'].sum()))
print('SHA256',hashlib.sha256(open(out,'rb').read()).hexdigest())
