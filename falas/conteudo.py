"""Textos atualizados a partir dos resultados: nenhum número inferencial duplicado à mão."""
import json
from pathlib import Path

R = json.loads((Path(__file__).resolve().parent.parent / 'saida/resultados.json').read_text(encoding='utf-8'))


def br(x, n=2):
    return f'{x:.{n}f}'.replace('.', ',')


def pval(x):
    return 'menor que 0,001' if x < .001 else br(x, 3)


def intervalo(ic, n=1):
    return f"{br(ic['li'], n)} a {br(ic['ls'], n)}"


q3, q4, q5 = R['q3_teste'], R['q4_ideb']['t'], R['q5_salario']['t']
pb, rn = R['q3_ic']['PB'], R['q3_ic']['RN']
limite = ('Os sorteios originais foram preservados: 30 municípios entre 217 elegíveis na PB e 161 no RN. '
          'Seis municípios por estado sem IDEB tiveram chance zero; não generalizamos automaticamente a todos os municípios.')
confianca = ('Em repetidas amostragens pelo mesmo desenho, um procedimento bem calibrado de 95% cobre o parâmetro '
             'em aproximadamente 95% dos casos. Aqui usamos aproximação t; 30 observações não garantem normalidade '
             'nem cobertura exata. A presença do parâmetro em um intervalo não prova representatividade.')
cpf = ('Como sorteamos sem reposição uma fração relevante da base, usamos EP = s/raiz(n) vezes raiz(1-n/M). '
       'M é 217 na PB e 161 no RN. A correção vale para a base elegível, não corrige a exclusão dos sem IDEB.')
renda = ('Cada município pesa igual. Estimamos a média dos percentuais municipais, não a proporção de pessoas '
         'do estado. Para esta última seriam necessários totais e denominadores compatíveis com o indicador e '
         'um estimador ponderado pelo desenho. A adaptação da questão 3 deve ser alinhada com a docente.')
normalidade = ('n=30 não é uma garantia. Assimetria, valores extremos e tamanho da população influenciam a aproximação. '
               'Os testes F clássicos pressupõem normalidade e são sensíveis a desvios; Shapiro e Levene são diagnósticos, '
               'não certificados de validade. Apresentamos resultados aproximados e a sensibilidade sem CPF no relatório.')
conceitos_comuns = [('População-alvo', limite), ('Correção de população finita (CPF)', cpf),
                   ('Confiança de 95%', confianca), ('Indicador de baixa renda', renda)]
perguntas_comuns = [('Vocês estimam a proporção de pessoas do estado?', renda),
                    ('Por que limitar aos elegíveis?', limite),
                    ('Trinta municípios garantem normalidade?', normalidade)]

PARTES = [
    {
        'tema': 'Abertura, objetivo e metodologia', 'curto': 'objetivo e metodologia',
        'quadrante': 'superior esquerdo',
        'fala': [
            ('Olhe para a turma.', 'Boa tarde, professora e turma. Nós somos {todos}. Nosso trabalho compara indicadores municipais da Paraíba e do Rio Grande do Norte.'),
            ('Aponte para o objetivo.', 'Analisamos o IDEB dos anos iniciais da rede pública, o percentual municipal de população com renda de até meio salário mínimo por pessoa e o salário médio dos trabalhadores formais.'),
            ('Aponte para o fluxo das bases.', 'A PB tem 223 municípios e o RN tem 167. No sorteio original, foram excluídos seis municípios de cada estado sem IDEB, restando 217 e 161 elegíveis. Preservamos esse sorteio: 30 municípios de cada base, por amostragem aleatória simples, sem reposição e com semente fixa.'),
            ('Aponte para a ressalva da questão 3.', 'Nossas conclusões inferenciais se limitam às bases elegíveis. Na renda, estimamos a média dos percentuais municipais, e não diretamente o percentual de pessoas do estado. Essa é uma adaptação do enunciado que precisa ser alinhada com a professora.'),
            ('Aponte para métodos e QR code.', 'Usamos intervalos de 95% e comparações aproximadas a 5%, com correção de população finita. Os links das planilhas estão no QR code. Agora, {p2} apresenta as estatísticas descritivas.'),
        ],
        'conceitos': [('AAS sem reposição', 'Todas as amostras de 30 municípios da base elegível têm a mesma probabilidade. Nenhum município se repete.'),
                      ('Semente', '20261116 fixa a sequência do gerador; o manifesto original confere nomes, valores e ordem.')]+conceitos_comuns,
        'numeros': [('PB', '223 no estado; 217 elegíveis; 30 sorteados'), ('RN', '167 no estado; 161 elegíveis; 30 sorteados'), ('Semente', '20261116, preservada'), ('Níveis', '95% de confiança; 5% de significância')],
        'perguntas': [('Por que não sortear de novo?', 'Preservamos a amostra publicada para não trocar resultados após observá-los. A exclusão original é uma limitação explícita a alinhar com a docente.'),
                      ('Qual ferramenta?', 'Python com NumPy, pandas, SciPy e Matplotlib; Chrome/Edge para os PDFs.')]+perguntas_comuns,
    },
    {
        'tema': 'Estatísticas descritivas', 'curto': 'estatísticas descritivas', 'quadrante': 'superior direito',
        'fala': [
            ('Aponte para a tabela.', 'A tabela compara as populações descritivas com as amostras de trinta municípios, nas linhas sombreadas. Na população descritiva usamos todos os municípios com cada indicador disponível; ela pode ser maior que a base do sorteio.'),
            ('Aponte para o IDEB.', 'No IDEB, a média da PB foi 5,57 na amostra e 5,34 nos municípios com dado. No RN, foi 4,85 e 4,84. A amostra da PB incluiu Coxixola, com IDEB 8,2. Essas diferenças mostram a variação que um sorteio pode produzir.'),
            ('Aponte para renda e salário.', 'As médias dos percentuais de baixa renda ficam perto de cinquenta por cento. Cada município pesa igual: esse número não é o percentual estadual de pessoas. Os salários médios ficam perto de 1,8 salário mínimo.'),
            ('Aponte para o desvio padrão.', 'Nos dados completos disponíveis, o RN apresenta maior dispersão salarial, com desvio padrão 0,31 contra 0,23. A PB apresenta maior dispersão no IDEB: 0,82 contra 0,66.'),
            ('Aponte para a interpretação e passe a palavra.', 'IDEB e salário têm assimetria positiva, com valores altos na cauda direita. Na renda das populações descritivas, a assimetria é negativa. A proximidade das médias não prova representatividade. Agora, {p3} mostra os gráficos e intervalos.'),
        ],
        'conceitos': [('Média e mediana', 'Média é soma dividida pela quantidade; mediana é o centro da lista ordenada. A média é mais sensível a extremos.'),
                      ('Variância', 'A tabela descritiva divide por N na população e n-1 na amostra. s² estima a variância finita definida com divisor M-1; para a média, usamos também a CPF.'),
                      ('Quartis e moda', 'Quartis interpolados pelo tipo 7. Moda omitida conforme orientação didática para medidas contínuas; é possível contar empates nos valores arredondados, mas isso não identifica uma moda exata da medida subjacente.')]+conceitos_comuns,
        'numeros': [('IDEB médio (amostras)', 'PB 5,57; RN 4,85'), ('Renda média municipal (amostras)', 'PB 51,01%; RN 48,87%'), ('Salário médio (amostras)', 'PB 1,78 SM; RN 1,88 SM'), ('Desvio padrão salarial descritivo', 'PB 0,23 SM; RN 0,31 SM')],
        'perguntas': [('Por que a média amostral não coincide com a populacional?', 'Há variação de amostragem. Um único sorteio não reproduz exatamente todas as características da base.'),
                      ('Maior dispersão salarial significa maior desigualdade entre pessoas?', 'Não. São diferenças de salários médios entre municípios; não medimos a distribuição de salários individuais.')]+perguntas_comuns,
    },
    {
        'tema': 'Gráficos dos salários e intervalos da renda', 'curto': 'gráficos e intervalos',
        'quadrante': 'inferior esquerdo',
        'fala': [
            ('Aponte para os histogramas e boxplots.', 'Agora vou mostrar os gráficos dos salários. As barras contam os municípios em cada faixa. No boxplot, a caixa reúne os cinquenta por cento centrais, a linha marca a mediana e o losango marca a média.'),
            ('Aponte primeiro para PB, depois RN.', 'A Paraíba é mais concentrada: vinte e quatro dos trinta municípios estão entre 1,6 e 1,9 salários mínimos. No Rio Grande do Norte, os valores estão mais espalhados, de 1,4 a 2,9 salários mínimos.'),
            ('Aponte para os pontos isolados.', 'Os dois gráficos têm assimetria à direita. Os pontos atípicos são Carrapateira, na PB, com 2,4 salários mínimos, e Riachuelo, no RN, com 2,9. Eles foram mantidos: ser atípico não significa que o dado esteja errado.'),
            ('Aponte para os intervalos corrigidos.', f"Na renda, comparamos a média dos percentuais municipais. Ela foi de {br(pb['media'],1)} por cento na PB e {br(rn['media'],1)} por cento no RN. Os intervalos de confiança de noventa e cinco por cento vão de {intervalo(pb)} por cento na PB e de {intervalo(rn)} por cento no RN."),
            ('Aponte para a fórmula e passe a palavra.', 'Usamos correção de população finita porque o sorteio foi sem reposição. Cada município tem o mesmo peso, e os resultados valem para as bases elegíveis, não diretamente para a proporção de pessoas de todo o estado. Agora, {p4} apresenta os testes.'),
        ],
        'conceitos': [('Histograma e boxplot', 'O histograma conta por faixa de 0,2 SM. A caixa vai de Q1 a Q3 e contém os 50% centrais; a linha é a mediana e o losango é a média.'),
                      ('Atípicos', 'Acima de Q3 + 1,5 × (Q3-Q1) ou abaixo de Q1 - 1,5 × (Q3-Q1). Limites superiores: PB 2,31 SM e RN 2,56 SM. Não indicam erro nem explicam causas.'),
                      ('Pontos percentuais', '51% menos 49% são 2 pontos percentuais, não 2% de aumento relativo.')]+conceitos_comuns,
        'numeros': [('Salários PB', '1,3 a 2,4 SM; DP 0,20; 24 municípios entre 1,6 e 1,9'), ('Salários RN', '1,4 a 2,9 SM; DP 0,30'),
                    ('Atípicos', 'Carrapateira 2,4 SM; Riachuelo 2,9 SM'),
                    ('Renda PB: média e IC com CPF', f"{br(pb['media'])}%; {intervalo(pb,2)}%"),
                    ('Renda RN: média e IC com CPF', f"{br(rn['media'])}%; {intervalo(rn,2)}%")],
        'perguntas': [('Por que os intervalos antigos eram muito largos?', 'A versão anterior aplicava variância binomial a percentuais municipais. Corrigimos para a variância observada entre municípios e incorporamos o sorteio sem reposição.'),
                      ('O que os triângulos indicam?', 'As médias conhecidas das bases elegíveis, usadas somente para comparação. Não são proporções estaduais de indivíduos e sua cobertura não prova representatividade.'),
                      ('A sobreposição dos ICs decide o teste?', 'Não. Para comparar médias, usamos o intervalo da diferença e o teste correspondente; dois ICs individuais podem se sobrepor mesmo quando o teste rejeita igualdade.')]+perguntas_comuns,
    },
    {
        'tema': 'Testes de hipóteses e conclusão', 'curto': 'testes e conclusão', 'quadrante': 'inferior direito',
        'fala': [
            ('Aponte para a tabela de testes.', 'Comparamos as médias com nível de significância de cinco por cento. A hipótese nula diz que as médias são iguais; a alternativa diz que são diferentes. Usamos as variâncias de cada estado separadamente e correção de população finita, com calibração t aproximada.'),
            ('Aponte para renda e IDEB.', f"Na média dos percentuais municipais de baixa renda, a diferença PB menos RN foi de {br(q3['diferenca'])} pontos percentuais, com p-valor {pval(q3['p_valor'])}. No IDEB, a diferença foi de {br(q4['diferenca'])} ponto, com p-valor {pval(q4['p_valor'])}. Há evidência de médias maiores na PB nessas duas comparações, nas bases elegíveis."),
            ('Aponte para salário.', f"No salário, o p-valor foi {pval(q5['p_valor'])}. Não encontramos evidência suficiente de diferença nas médias. Isso não prova igualdade."),
            ('Aponte para os diagnósticos.', 'Como solicitado, também comparamos variâncias. O F clássico não rejeita igualdade no IDEB e rejeita no salário. Mas ele é sensível à falta de normalidade, e o diagnóstico de Levene não rejeita no salário. Por isso, não usamos o F como escolha automática do teste principal.'),
            ('Aponte para a conclusão.', 'Concluímos que o IDEB e a média municipal de baixa renda foram maiores na PB, enquanto a comparação salarial foi inconclusiva. O RN teve maior dispersão salarial observada. Os resultados são aproximados, limitados aos elegíveis, e não identificam causas. A adaptação da questão três precisa ser alinhada com a professora. Obrigado.'),
        ],
        'conceitos': [('p-valor', 'Sob H0 e as condições do método, probabilidade de obter estatística tão extrema ou mais que a observada. Não é a probabilidade de H0 ser verdadeira.'),
                      ('Teste principal', 'Variância estimada da diferença = (1-n/M_PB)s²_PB/n + (1-n/M_RN)s²_RN/n. Usa t aproximado com gl de Satterthwaite; não é um teste exato sob qualquer população finita.'),
                      ('F e Levene', 'F clássico pressupõe normalidade iid e tem sensibilidade aos extremos. Levene com centro na mediana é menos sensível. São diagnósticos complementares; não provaram igualdade.'),
                      ('Normalidade', normalidade)]+conceitos_comuns,
        'numeros': [(titulo, f"t = {br(t['t'])}; gl ≈ {br(t['gl'],1)}; p {pval(t['p_valor'])}; IC diferença {br(t['ic_dif_li'])} a {br(t['ic_dif_ls'])}") for titulo,t in [('Renda (p.p.)',q3),('IDEB (ponto)',q4),('Salário (SM)',q5)]] + [('F clássico', 'IDEB: p 0,303; salário: p 0,026. Levene salário: p 0,097.')],
        'perguntas': [('Por que não escolher automaticamente o teste pelo F?', 'Não rejeitar igualdade não a comprova, F é sensível à não normalidade e o pré-teste não fornece garantia de validade. A análise principal não exige variâncias iguais.'),
                      ('Isso explica o IDEB?', 'Não. Comparações de médias separadas não estimam efeitos nem controlam fatores de confusão.'),
                      ('Por que o p-valor mudou desde o roteiro anterior?', 'Corrigimos o parâmetro da renda e a variância do estimador. A CPF também altera os erros padrão de todas as médias; a amostra é a mesma.')]+perguntas_comuns,
    },
]
COMUM = [limite, renda, normalidade,
         f"Comparações principais com CPF: renda p {pval(q3['p_valor'])}; IDEB p {pval(q4['p_valor'])}; salário p {pval(q5['p_valor'])}.",
         'Não interpretamos cobertura de IC como prova de representatividade e não afirmamos relações causais.',
         'Ordem: {p1}, {p2}, {p3}, {p4}.']
DICAS = ['Ensaiem juntos, apontando para o cartaz atualizado.',
         'Use os números do cartaz novo; os PDFs e roteiros anteriores foram substituídos.',
         'Se esquecer um número, consulte o cartaz. Explique a ideia com calma.',
         'Confiram o acesso público ao link das planilhas e alinhem a adaptação com a docente.']
