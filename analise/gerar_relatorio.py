"""Gera o relatório em português a partir dos resultados corrigidos."""
import json
from pathlib import Path

RAIZ=Path(__file__).resolve().parent.parent
R=json.loads((RAIZ/'saida/resultados.json').read_text(encoding='utf-8'))

def br(x,n=2):
    return f'{x:.{n}f}'.replace('.',',')

def pv(x):
    return '< 0,001' if x<.001 else br(x,3)

texto='''# Projeto da Unidade II: IDEB, baixa renda e salário (PB × RN)

UFPB · Métodos Estatísticos Aplicados às Ciências Tecnológicas · Docente: Renilma Pereira.
Integrantes: Augusto Blois, Pedro Luna, Luy Koji e Luiz Ramalho. Apresentação: 16/11/2026.

## 1. Revisão e adaptação do enunciado

A questão 3 foi corrigida: a unidade sorteada é o município, com um percentual numérico, e não uma pessoa com resposta binária. A fórmula binomial não é adequada para a variância da média desses percentuais. Estimamos a **média não ponderada dos percentuais municipais de população com renda per capita até meio salário mínimo**. Esta é uma adaptação do enunciado **a alinhar com a docente**; não equivale à proporção de indivíduos de cada estado.

Para estimar a proporção de indivíduos seriam necessários totais e denominadores compatíveis com o indicador e com seu ano, e estimadores de totais/razão que considerem a seleção dos municípios. Uma média simples não dá mais peso a municípios populosos.

Nenhum sorteio foi trocado. Semente 20261116; NumPy default_rng, PB primeiro e RN depois, sem reposição; mesmos nomes, valores e ordem do projeto original. `dados/amostra_original.json` preserva o manifesto de auditoria, e a análise interrompe a execução se houver divergência. Repositório de origem: augustoblois/metodos-estatisticos-projeto-un2, commit eb8c74e08e4d9818bc5beaaba0d7753a89eb893c.

## 2. População descritiva, base de sorteio e alcance

As planilhas originais contêm 223 municípios da PB e 167 do RN. Seis de cada estado não têm IDEB e foram excluídos **antes do sorteio original**. Isso produz bases de 217 e 161 municípios, com 30 sorteados em cada uma. Cada amostra possível de tamanho 30 da base elegível tem igual probabilidade; os excluídos têm probabilidade zero. Portanto, não é AAS de todos os 223/167 como solicitado originalmente.

Preservamos essa escolha e a documentamos, sem supor que a falta de IDEB seja aleatória. A inferência refere-se somente às bases elegíveis. A docente deve avaliar também essa adaptação. Para cumprir literalmente o sorteio de todos, seria necessário definir previamente um tratamento dos dados ausentes, com autorização e nova documentação; isso não foi feito nesta revisão.

As tabelas descritivas continuam usando todos os valores disponíveis de cada indicador: IDEB em 217/161; renda e salário em 223/167. As referências nos gráficos inferenciais são sempre as médias das **bases elegíveis de 217/161**, evitando comparar estimador e parâmetro de universos diferentes. O JSON registra também as descritivas dessas bases.

As planilhas fornecidas não informam os anos de referência dos indicadores. Não pressupomos que sejam contemporâneos, e essa limitação impede interpretações temporais ou causais.

Municípios sem IDEB excluídos:
'''
for uf in ('PB','RN'):
    texto+=f"\n- **{uf}:** "+', '.join(R['sem_ideb'][uf])+'.\n'
texto+='''
## 3. Questão 1: estatísticas descritivas

Variância descritiva da população: divisor N; amostral: n−1. Quartis por interpolação linear, tipo 7. Moda omitida conforme a orientação didática para medidas contínuas; empates nos dados arredondados podem ser contados, mas não identificam uma moda pontual da medida original. A variância s² com divisor n−1 estima a variância finita S² com divisor M−1; a variância populacional descritiva com divisor M é outro parâmetro: σ² = (M−1)S²/M.
'''
for var,titulo in [('ideb','IDEB dos anos iniciais da rede pública'),('renda','Percentual municipal de baixa renda (%)'),('salario','Salário médio formal (SM)')]:
    texto+=f'\n### {titulo}\n\n| Estado / conjunto | n | Média | Mediana | Variância | DP | Mín. | Q1 | Q3 | Máx. | Assimetria |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
    for uf in ('PB','RN'):
        for conjunto in ('populacao','amostra'):
            d=R['descritivas'][uf][conjunto][var]
            valores=[str(d['n'])]+[br(d[k],3 if k=='variancia' else 2) for k in ('media','mediana','variancia','dp','minimo','q1','q3','maximo','assimetria')]
            texto+='| '+uf+' / '+('população descritiva' if conjunto=='populacao' else 'amostra')+' | '+' | '.join(valores)+' |\n'
texto+='''
**Interpretação.** O IDEB médio é maior na PB tanto na amostra quanto no conjunto com dado. A amostra da PB inclui valores altos, como Coxixola (8,2), Cabaceiras (7,7) e Cubati (7,1), elevando sua média de 5,57 em relação a 5,34. O RN tem maior dispersão salarial entre municípios (DP populacional descritivo 0,31 contra 0,23 SM); a PB tem maior dispersão do IDEB (0,82 contra 0,66). As médias municipais de baixa renda estão próximas de 50%, sem equivaler à proporção estadual de pessoas. IDEB e salários têm assimetria positiva; renda nas populações descritivas tem coeficiente negativo. Média próxima da mediana, isoladamente, não prova simetria. Proximidade entre amostra e população também não prova representatividade.

## 4. Questão 2: histogramas e boxplots dos salários

Histogramas com classes de 0,2 SM, fechadas à esquerda; a última inclui o extremo direito. Mesmas escalas para os estados. Boxplot: caixa de Q1 a Q3, linha na mediana, losango na média e bigodes nos extremos não atípicos. Regra: valores abaixo de Q1−1,5·AIQ ou acima de Q3+1,5·AIQ; AIQ=Q3−Q1.

Na PB, 24 dos 30 salários médios municipais estão entre 1,6 e 1,9 SM. O intervalo observado é 1,3 a 2,4 SM e o DP é 0,20. No RN, o intervalo é 1,4 a 2,9 SM e o DP é 0,30. A dispersão maior do RN aparece também na caixa: AIQ 0,375 contra 0,275 SM. Assimetria positiva nas duas amostras, mais forte no RN. Carrapateira (PB, 2,4 SM) e Riachuelo (RN, 2,9 SM) superam os limites superiores de 2,3125 e 2,5625 SM. São observações mantidas; o boxplot não prova erro nem explica a causa. Não medimos desigualdade salarial entre indivíduos.

## 5. Inferência com população finita

Seja M o número de municípios na base elegível, n=30, e s² a variância amostral com divisor n−1. Sob AAS sem reposição:

`V̂(x̄) = (1 − n/M) s²/n` e `EP(x̄) = sqrt(V̂(x̄))`.

Usamos `IC ≈ x̄ ± t(0,975; n−1) EP(x̄)`. A variância estimada é de desenho; a calibração t é **aproximada**, não uma distribuição exata garantida para qualquer população finita. Não usamos a fórmula sqrt((M−n)/(M−1)) com s²/n, pois isso misturaria convenções de variância; com s² definido por n−1 a CPF no EP é sqrt(1−n/M).
'''
for uf in ('PB','RN'):
    ic=R['q3_ic'][uf]
    texto+=f"\n- {uf}: M={ic['M']}, fração amostral {br(100*ic['fracao_amostral'])}%, CPF no EP={br(ic['fpc'],6)}.\n"
texto+='''
Para comparar bases sorteadas separadamente, a estimativa da variância da diferença é a soma dos componentes `a=(1−n1/M1)s1²/n1` e `b=(1−n2/M2)s2²/n2`. A estatística é `t=(x̄1−x̄2)/sqrt(a+b)`; graus de liberdade aproximados `ν=(a+b)²/[a²/(n1−1)+b²/(n2−1)]` (calibração de Satterthwaite). É uma comparação aproximada de desenho com variâncias separadas e CPF, não o Welch iid padrão nem um teste exato de populações finitas. Para todas as médias, α=5%, H0: μ_PB=μ_RN; H1: μ_PB≠μ_RN. Não há correção por múltiplas comparações; as decisões são por comparação.

### Questão 3: média dos percentuais municipais

Unidade: pontos percentuais do indicador municipal. Não há Bernoulli individual nem contagem de sucessos entre 30 pessoas.

| Base | Média (%) | EP (p.p.) | Margem (p.p.) | IC aproximado 95% (%) | Média conhecida da base elegível (%) |
|---|---:|---:|---:|---|---:|
'''
for uf in ('PB','RN'):
    ic=R['q3_ic'][uf]
    texto+=f"| {uf} | {br(ic['media'])} | {br(ic['ep'],4)} | {br(ic['erro'])} | {br(ic['li'])} a {br(ic['ls'])} | {br(ic['valor_real'])} |\n"
texto+='\n### Comparações principais das questões 3, 4 e 5\n\n| Indicador | Diferença PB−RN | EP | t aproximado | gl | p-valor | IC 95% da diferença | Decisão a 5% |\n|---|---:|---:|---:|---:|---:|---|---|\n'
for var,titulo,teste in [('renda','Baixa renda (p.p.)',R['q3_teste']),('ideb','IDEB (ponto)',R['q4_ideb']['t']),('salario','Salário (SM)',R['q5_salario']['t'])]:
    dec='Rejeita H0; PB maior' if teste['rejeita_h0'] else 'Não rejeita H0'
    texto+=f"| {titulo} | {br(teste['diferenca'])} | {br(teste['ep'],4)} | {br(teste['t'])} | {br(teste['gl'],2)} | {pv(teste['p_valor'])} | {br(teste['ic_dif_li'])} a {br(teste['ic_dif_ls'])} | {dec} |\n"
texto+='''
**Interpretação:** há evidência de média municipal de baixa renda maior na PB e de IDEB médio maior na PB, dentro das bases elegíveis e sob a aproximação adotada. Não há evidência suficiente de diferença salarial média; isso não demonstra igualdade. A sobreposição de ICs individuais não substitui o teste da diferença. Resultados são descritivos/inferenciais, sem identificação de causas ou efeitos de políticas.

### Questões 4 e 5: diagnóstico de variâncias solicitado

F clássico: H0: σ²_PB=σ²_RN; H1: diferentes; gl=(29,29), sob modelo normal iid. Os p-valores a seguir são diagnósticos de modelo, não p-valores exatos sob o desenho finito. Levene usa centro na mediana e é menos sensível à não normalidade, mas também não é livre de pressupostos.

| Indicador | F | p F | p Levene | p Shapiro PB | p Shapiro RN |
|---|---:|---:|---:|---:|---:|
'''
for chave,titulo in [('q4_ideb','IDEB'),('q5_salario','Salário')]:
    d=R[chave]
    texto+=f"| {titulo} | {br(d['f']['f'])} | {pv(d['f']['p_valor'])} | {pv(d['levene_p'])} | {pv(d['shapiro_p']['PB'])} | {pv(d['shapiro_p']['RN'])} |\n"
texto+='''
No IDEB, F não rejeita igualdade; isso não a prova. No salário, F rejeita, enquanto Levene não rejeita, indicando sensibilidade à modelagem. A comparação principal usa variâncias separadas e CPF nas três variáveis e não depende da seleção automática por um pré-teste F. Para atender à abordagem didática do enunciado, os testes t clássicos escolhidos pelo F e o outro teste t ficam documentados como sensibilidade, sem CPF.

**Normalidade:** n=30 não garante distribuição normal da média nem validade automática dos testes. A aproximação depende de assimetria, extremos e frações amostrais. Shapiro detecta desvios no salário e no IDEB do RN; na renda do RN também há assimetria. Os resultados devem ser interpretados com essas limitações. Não há promessa de cobertura exata de 95% ou de controle exato de 5% para estas populações.

### Sensibilidade: comparação clássica sem CPF

| Indicador | Método selecionado pelo F (apenas complemento) | p | p do outro teste t |
|---|---|---:|---:|
'''
for titulo,d in [('Renda',R['q3_diagnosticos']),('IDEB',R['q4_ideb']),('Salário',R['q5_salario'])]:
    t=d['classico_sem_cpf']; metodo='t combinado, variâncias iguais' if t['variancias_iguais'] else 'Welch, variâncias separadas'
    texto+=f"| {titulo} | {metodo} | {pv(t['p_valor'])} | {pv(d['outro_t']['p_valor'])} |\n"
texto+='\nAs decisões a 5% não mudam com ou sem CPF neste conjunto de dados. Os ICs t individuais sem CPF na renda são 49,67–52,35% (PB) e 47,55–50,18% (RN); os novos ICs principais são mais estreitos por incorporarem o sorteio sem reposição.\n'
texto+='\n### ICs complementares de IDEB e salário, com CPF\n\n| Indicador/base | Média | IC 95% aprox. | Referência elegível |\n|---|---:|---|---:|\n'
for var in ('ideb','salario'):
    for uf in ('PB','RN'):
        ic=R['ic_medias'][var][uf]
        texto+=f"| {var} / {uf} | {br(ic['media'])} | {br(ic['li'])} a {br(ic['ls'])} | {br(ic['valor_real'])} |\n"
texto+='''
As referências conhecidas permitem conferir este sorteio; conter a referência em um intervalo não prova representatividade, validade do método ou ausência de viés de cobertura. Como os dados completos das bases estão disponíveis, suas médias são conhecidas; a inferência amostral é um exercício didático de estimar parâmetros usando somente a amostra. Os parâmetros não foram usados para estimar os erros padrão.

## 6. Apresentação e impressão

1. Augusto: objetivo, desenho, exclusões e adaptação da questão 3.
2. Pedro: estatísticas descritivas e alcance da comparação.
3. Luy: histogramas, boxplots e ICs corrigidos da renda.
4. Luiz: testes, diagnósticos e conclusão sem causalidade.

Os roteiros completos estão em `falas/falas (Nome).pdf`; os textos curtos em `falas/fala_simples_Nome.md`. Todos são gerados a partir de `saida/resultados.json`, usando `falas/conteudo.py`. A fala de Luy inclui indicações de onde apontar, números atualizados e respostas a perguntas prováveis.

Imprimir o `cartaz/cartaz_4xA4.pdf` em 100% (quatro folhas A4, 2×2), ou `cartaz_2xA3.pdf` (duas A3), ou `cartaz_A2.pdf` em uma A2. Colar em cartolina ou suporte semelhante, conforme o enunciado. Conferir todos os nomes e o QR code antes de imprimir.

O link externo das planilhas foi preservado; esta revisão não altera conteúdo nem permissões do Google Drive. O grupo deve conferir o acesso sem login e atualizar a versão da planilha, se necessário. As amostras numéricas não mudaram.

## 7. Reproduzir e conferir

Requer Python 3.12 e Chrome ou Edge. Na pasta do projeto, execute `powershell -ExecutionPolicy Bypass -File reproduzir.ps1` (a opção vale somente para esse processo). O script cria um ambiente local `.venv`, instala `requirements.txt`, executa análise, relatório, cartaz, falas e verificação. Não publica no GitHub.

Também é possível executar manualmente no ambiente preparado:

```powershell
python analise/analise.py
python analise/gerar_relatorio.py
python cartaz/montar_cartaz.py
python falas/gerar_falas.py
python analise/verificar.py
```

`saida/verificacao.json` contém as verificações de integridade da amostra, fórmulas, decisões e PDFs. Os gráficos são PNG e SVG. O cartaz é montado a partir de `cartaz/modelo.html`; não editar somente o HTML gerado nem somente um PDF, pois a próxima geração substituirá essas alterações.

## 8. Referências metodológicas

- [Penn State STAT 506: média e total sob AAS sem reposição](https://online.stat.psu.edu/stat506/Lesson01): variância estimada da média e correção finita.
- [NIST: comparação de duas médias](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm): variâncias separadas e graus de liberdade de Welch-Satterthwaite. A inclusão da CPF é a extensão aproximada de desenho explicitada neste relatório.
- [NIST: intervalo para média](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm): calibração t e interpretação de confiança.
- [NIST: proporções binomiais](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm): a fórmula binomial é para contagens de sucessos, não para a variância empírica de percentuais municipais.
- IBGE Cidades e Estados; dados usados: planilhas originais fornecidas pela docente, preservadas em `dados-originais/`.
'''
(RAIZ/'RELATORIO.md').write_text(texto,encoding='utf-8')
print('RELATORIO.md atualizado a partir dos resultados.')
