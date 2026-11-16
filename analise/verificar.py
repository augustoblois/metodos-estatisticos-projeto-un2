"""Verifica integridade dos dados, cálculos de desenho e artefatos gerados."""
import importlib.util
import json
import math
from pathlib import Path

import fitz
import numpy as np
import pandas as pd
from scipy import stats

RAIZ=Path(__file__).resolve().parent.parent
R=json.loads((RAIZ/'saida/resultados.json').read_text(encoding='utf-8'))
manifesto=json.loads((RAIZ/'dados/amostra_original.json').read_text(encoding='utf-8'))
checks=[]

def exigir(condicao, nome):
    if not condicao:
        raise AssertionError(nome)
    checks.append(nome)

exigir(R['amostras']==manifesto['amostras'] and R['semente']==manifesto['semente'], 'Mesmos 60 municípios, dados, ordens e semente do original')
spec=importlib.util.spec_from_file_location('projeto_analise',RAIZ/'analise/analise.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
for uf,aba in [('PB','Amostra 1 - PB'),('RN','Amostra 2 - RN')]:
    am=R['amostras'][uf]; m=R['tamanho_base_sorteio'][uf]; n=len(am)
    exigir(n==30 and len({x['municipio'] for x in am})==30, f'{uf}: 30 municípios únicos')
    df=pd.read_excel(RAIZ/'dados/amostras.xlsx',sheet_name=aba)
    exigir(df.iloc[:,1].tolist()==[x['municipio'] for x in am], f'{uf}: nomes iguais na planilha original')
    exigir(np.allclose(df.iloc[:,2:5].to_numpy(dtype=float),[[x[k] for k in ('ideb','renda','salario')] for x in am]),f'{uf}: valores iguais na planilha original')
    for var in ('renda','ideb','salario'):
        x=np.array([d[var] for d in am])
        ic=R['q3_ic'][uf] if var=='renda' else R['ic_medias'][var][uf]
        # Referência independente: soma dos desvios, sem chamar a função de produção.
        s2=sum((v-sum(x)/n)**2 for v in x)/(n-1)
        ep=math.sqrt((1-n/m)*s2/n)
        exigir(math.isclose(ep,ic['ep'],rel_tol=1e-12),f'{uf}/{var}: EP com CPF conferido independentemente')
        exigir(math.isclose(ic['ls']-ic['media'],stats.t.ppf(.975,n-1)*ep,rel_tol=1e-12),f'{uf}/{var}: margem e quantil t')
        exigir(ic['valor_real']==R['descritivas_base_elegivel'][uf][var]['media'],f'{uf}/{var}: referência é a base elegível')
        exigir(ic['M']==m and ic['ep']<math.sqrt(s2/n),f'{uf}/{var}: população e efeito da CPF coerentes')

for var,t in [('renda',R['q3_teste']),('ideb',R['q4_ideb']['t']),('salario',R['q5_salario']['t'])]:
    componentes=[]
    for uf in ('PB','RN'):
        vals=[x[var] for x in R['amostras'][uf]]; n=len(vals); mu=sum(vals)/n
        s2=sum((x-mu)**2 for x in vals)/(n-1)
        componentes.append((1-n/R['tamanho_base_sorteio'][uf])*s2/n)
    ep=math.sqrt(sum(componentes)); gl=sum(componentes)**2/sum(c*c/29 for c in componentes)
    exigir(math.isclose(ep,t['ep'],rel_tol=1e-12) and math.isclose(gl,t['gl'],rel_tol=1e-12),f'{var}: variância da diferença e gl conferidos')
    p=2*stats.t.sf(abs(t['diferenca']/ep),gl)
    exigir(math.isclose(p,t['p_valor'],rel_tol=1e-12),f'{var}: p-valor conferido')
    exigir(t['rejeita_h0']==(t['ic_dif_li']>0 or t['ic_dif_ls']<0),f'{var}: teste e IC da diferença concordam')

# Caso com enumeração exata: valida a convenção da CPF, além dos dados do projeto.
from itertools import combinations
pop=np.array([1.,2.,4.,7.,11.]); amostras=np.array(list(combinations(pop,3)))
variancia_exata=np.var(amostras.mean(axis=1),ddof=0)
estimativas=(1-3/5)*np.var(amostras,axis=1,ddof=1)/3
exigir(np.isclose(estimativas.mean(),variancia_exata),'CPF: média dos estimadores coincide com a variância exata de todas as amostras')
ic_censo=mod.ic_media_finita(pop,5,pop.mean())
exigir(ic_censo['ep']==0 and ic_censo['li']==ic_censo['ls']==pop.mean(),'CPF: limite censitário tem erro padrão zero')

pdfs={'cartaz/cartaz_A2.pdf':1,'cartaz/cartaz_4xA4.pdf':4,'cartaz/cartaz_2xA3.pdf':2}
for nome in ('Augusto Blois','Pedro Luna','Luy Koji','Luiz Ramalho'):
    pdfs[f'falas/falas ({nome}).pdf']=None
pdf_info={}
proibidos=['33,1%','68,9%','66,8%','0,868','17,9 pontos','não parece vir','representaram bem','n=30 garante normalidade']
for caminho,n_pag in pdfs.items():
    with fitz.open(RAIZ/caminho) as doc:
        exigir(len(doc)>0 and (n_pag is None or len(doc)==n_pag),f'{caminho}: número de páginas')
        texto='\n'.join(p.get_text() for p in doc)
        exigir(len(texto)>100,f'{caminho}: texto extraível')
        exigir(not any(t in texto for t in proibidos),f'{caminho}: sem resultados antigos ou frases retiradas')
        for i,p in enumerate(doc):
            exigir(bool(p.get_text().strip()),f'{caminho}: página {i+1} não vazia')
            # Detecta texto para fora da página (tolerância para diferenças de fonte).
            spans=[s for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
            exigir(all(s['bbox'][0]>=-1 and s['bbox'][1]>=-1 and s['bbox'][2]<=p.rect.width+1 and s['bbox'][3]<=p.rect.height+1 for s in spans),f'{caminho}: página {i+1} com texto dentro dos limites')
        pdf_info[caminho]={'paginas':len(doc),'dimensoes_pt':[[round(p.rect.width,2),round(p.rect.height,2)] for p in doc]}

for arquivo in ('ic_renda_media','medias_ic','salario_hist_boxplot'):
    exigir(all((RAIZ/'saida/graficos'/f'{arquivo}.{ext}').stat().st_size>1000 for ext in ('png','svg')),f'{arquivo}: PNG e SVG gerados')

resultado={'status':'aprovado','checagens':checks,'pdfs':pdf_info,
           'limites':'Conferência computacional não garante normalidade/cobertura exata nem acesso público ao Drive. Inspeção visual complementar executada na entrega.'}
(RAIZ/'saida/verificacao.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'APROVADO: {len(checks)} verificações; amostra preservada, cálculos e PDFs coerentes.')
