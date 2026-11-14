# -*- coding: utf-8 -*-
"""
Gera um PDF de falas para cada integrante do grupo.

Lê os nomes de cartaz/config.json e as imagens do cartaz pronto (cartaz/cartaz_A2.pdf).
Gera, dentro da pasta falas/:
  falas (Nome Sobrenome).pdf   um por integrante, em A5 (lê bem no celular e imprime bem)

A ordem de quem fala segue a ordem dos nomes no config.json: o 1º nome faz a parte 1
(quadrante superior esquerdo), o 2º a parte 2, e assim por diante.

Como rodar (PowerShell, dentro da pasta projeto-un2), depois de gerar o cartaz:
    python falas\\gerar_falas.py
"""
import base64
import html
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from string import Template

import fitz  # PyMuPDF: tira as imagens do cartaz e confere os PDFs

PASTA = Path(__file__).resolve().parent  # projeto-un2/falas
RAIZ = PASTA.parent
CFG = json.loads((RAIZ / "cartaz" / "config.json").read_text(encoding="utf-8-sig"))
CARTAZ = RAIZ / "cartaz" / "cartaz_A2.pdf"
NAVEGADORES = [Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
               Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")]
PALAVRAS_POR_MINUTO = 140  # ritmo calmo de apresentação

# ---------------------------------------------------------------- conteúdo
# {p1} a {p4} viram o primeiro nome de quem faz cada parte; {todos} vira a lista dos primeiros nomes.
# Os números são os do cartaz (saida/resultados.json, semente 20261116).
PARTES = [
    {
        "tema": "Abertura, objetivo e metodologia",
        "curto": "abertura, objetivo e metodologia",
        "quadrante": "superior esquerdo",
        "fala": [
            ("Olhe para a turma.",
             "Bom dia (ou boa tarde), professora e turma. Nós somos {todos}, e o nosso trabalho compara a "
             "Paraíba e o Rio Grande do Norte com dados do IBGE."),
            ("Aponte para a seção 1, Objetivo.",
             "O objetivo foi comparar os dois estados em três indicadores. O primeiro é o IDEB dos anos iniciais "
             "da rede pública, que mede a qualidade da educação numa escala de 0 a 10. O segundo é a porcentagem "
             "da população com renda per capita de até meio salário mínimo. O terceiro é o salário médio mensal "
             "dos trabalhadores formais, medido em salários mínimos. A pergunta do trabalho é: os dois estados "
             "são diferentes nesses indicadores?"),
            ("Aponte para o fluxo 223 → 217 → sorteio de 30 (PB) e 167 → 161 → sorteio de 30 (RN).",
             "A Paraíba tem 223 municípios, e o Rio Grande do Norte tem 167. Seis municípios de cada estado não "
             "têm IDEB divulgado. Como precisávamos das três variáveis de cada município, eles ficaram fora do "
             "sorteio, e sobraram 217 na Paraíba e 161 no Rio Grande do Norte."),
            ("Aponte para a linha Amostragem.",
             "De cada estado, sorteamos 30 municípios por amostragem aleatória simples, sem reposição. Isso quer "
             "dizer que todo município tinha a mesma chance de sair, e nenhum podia sair duas vezes. O sorteio foi "
             "feito no computador com uma semente fixa, então qualquer pessoa consegue refazer o sorteio e chegar "
             "exatamente nos mesmos municípios."),
            ("Aponte para as linhas Variáveis e Métodos.",
             "As três variáveis são quantitativas contínuas. Para analisar, usamos estatística descritiva, "
             "intervalos de confiança de 95% e testes de hipóteses, sempre com nível de significância de 5%."),
            ("Aponte para o QR code e passe a palavra.",
             "As planilhas com as duas amostras estão neste QR code. Agora, {p2} vai mostrar as estatísticas "
             "descritivas."),
        ],
        "conceitos": [
            ("População e amostra",
             "População é o conjunto inteiro que queremos estudar: aqui, todos os municípios de cada estado. "
             "Amostra é a parte que sorteamos para analisar: 30 municípios por estado. A estatística tira "
             "conclusões sobre a população olhando só a amostra. Neste trabalho conhecemos a população, então deu "
             "para conferir se a amostra acertou."),
            ("Amostragem aleatória simples (AAS)",
             "Todo município da lista tem a mesma chance de ser sorteado, como tirar 30 nomes de um saco sem olhar. "
             "Isso evita que a escolha favoreça algum tipo de município."),
            ("Sem reposição",
             "Depois que um município sai, ele não volta para o saco. Por isso a amostra tem 30 municípios "
             "diferentes."),
            ("Semente",
             "O computador gera os números aleatórios a partir de um número inicial, a semente. Com a mesma "
             "semente, o sorteio sai igual toda vez. A nossa é 20261116, a data da apresentação (16/11/2026)."),
            ("Variável quantitativa contínua",
             "Variável medida por números que podem ter qualquer valor dentro de uma faixa, como 5,34 de IDEB ou "
             "1,8 salário mínimo. Uma variável discreta seria uma contagem (número de escolas), e uma qualitativa "
             "seria uma categoria (a região do estado)."),
            ("IDEB",
             "Índice de Desenvolvimento da Educação Básica, calculado pelo governo federal. Junta a taxa de "
             "aprovação dos alunos com as notas em provas de português e matemática. Vai de 0 a 10, e quanto "
             "maior, melhor."),
            ("Renda per capita",
             "A renda de toda a casa dividida pelo número de moradores. A variável mostra a porcentagem dos "
             "moradores do município que vivem com até meio salário mínimo por pessoa."),
            ("Trabalhadores formais e SM",
             "Trabalhadores formais são os que têm emprego registrado, com carteira assinada ou como servidores "
             "públicos. O salário médio deles aparece em salários mínimos (SM): 1,8 SM quer dizer 1,8 vez o "
             "salário mínimo."),
            ("Nível de significância de 5%",
             "O risco que o grupo aceitou de dizer que existe diferença entre os estados quando ela não existe. "
             "{p4} explica os testes."),
            ("Intervalo de confiança de 95%",
             "Uma faixa de valores, calculada com a amostra, que contém o valor real da população em 95% dos "
             "sorteios possíveis. {p3} mostra os intervalos."),
        ],
        "numeros": [
            ("Paraíba", "223 municípios, 217 com as 3 variáveis, 30 sorteados"),
            ("Rio Grande do Norte", "167 municípios, 161 com as 3 variáveis, 30 sorteados"),
            ("Sem IDEB divulgado", "6 municípios em cada estado"),
            ("Semente do sorteio", "20261116 (a data da apresentação)"),
            ("Nível de significância", "5% (α = 0,05)"),
            ("Confiança dos intervalos", "95%"),
            ("Fonte dos dados", "IBGE Cidades e Estados, nas planilhas da professora"),
        ],
        "perguntas": [
            ("Por que 30 municípios?",
             "É o tamanho que o enunciado pede. Além disso, com 30 por estado, o Teorema Central do Limite garante "
             "que as médias se comportam de forma aproximadamente normal, o que sustenta os testes."),
            ("Por que vocês tiraram 6 municípios de cada estado?",
             "Eles não têm IDEB divulgado, e cada município da amostra precisava das três variáveis. Conferimos o "
             "efeito: sem eles, as médias de renda e salário mudam menos de 0,1."),
            ("Como vocês garantem que o sorteio foi aleatório?",
             "O computador sorteou com um gerador de números aleatórios. A semente fixa permite repetir o sorteio, "
             "e a planilha mostra a ordem em que cada município saiu."),
            ("Quais municípios foram sorteados?",
             "Estão na planilha do QR code. Alguns exemplos: Coxixola e Cabaceiras na Paraíba, Ipueira e "
             "Riachuelo no Rio Grande do Norte."),
            ("Por que amostragem aleatória simples, e não outro tipo?",
             "É a que o enunciado pede, e é a mais simples: cada município tem a mesma chance. Uma alternativa "
             "seria a estratificada, que sorteia separadamente dentro de grupos, por exemplo, as regiões do estado."),
            ("Vocês usaram o R?",
             "Usamos Python, com as bibliotecas pandas, SciPy e Matplotlib. As fórmulas são as mesmas que o R usa."),
        ],
    },
    {
        "tema": "Estatísticas descritivas",
        "curto": "estatísticas descritivas",
        "quadrante": "superior direito",
        "fala": [
            ("Aponte para a tabela inteira.",
             "Esta tabela mostra as estatísticas descritivas das três variáveis. Para cada estado, a linha branca "
             "é a população inteira, e a linha sombreada é a nossa amostra de 30 municípios. As colunas trazem a "
             "média, a mediana, a variância, o desvio padrão, o mínimo, os quartis e o máximo."),
            ("Aponte para as linhas do IDEB da PB (população e amostra).",
             "Comparando população e amostra, as médias da amostra ficaram perto das da população. A maior "
             "diferença relativa foi no IDEB da Paraíba: 5,57 na amostra contra 5,34 na população. Isso aconteceu "
             "porque o sorteio pegou alguns municípios com IDEB alto, como Coxixola, que tem 8,2, o maior do estado."),
            ("Aponte para as linhas da renda do RN.",
             "Os extremos da amostra costumam ser menos extremos que os da população. Na renda do RN, por exemplo, "
             "a amostra vai de 37,5% a 52,9%, enquanto a população vai de 35,5% a 61,4%."),
            ("Aponte para a coluna Média, comparando PB e RN.",
             "Comparando os estados, a Paraíba tem IDEB maior: 5,34 contra 4,84 na população. Já renda e salário "
             "têm centros parecidos. Nos dois estados, cerca de 50% da população tem renda de até meio salário "
             "mínimo, e o salário médio fica perto de 1,8 salário mínimo."),
            ("Aponte para a coluna Desvio padrão.",
             "Na dispersão, o RN varia mais no salário, com desvio padrão de 0,31 contra 0,23. A Paraíba varia "
             "mais no IDEB: 0,82 contra 0,66."),
            ("Aponte para o quadro “O que a tabela mostra”.",
             "Sobre a assimetria, IDEB e salário têm cauda à direita: a maioria dos municípios fica no meio, e "
             "poucos têm valores bem altos. A renda tem cauda à esquerda nas populações, com poucos municípios de "
             "porcentagem bem menor que os outros."),
            ("Aponte para a nota embaixo da tabela e passe a palavra.",
             "Não calculamos a moda, porque as três variáveis são quantitativas contínuas, como diz a observação "
             "do enunciado. Agora, {p3} vai mostrar os gráficos."),
        ],
        "conceitos": [
            ("Média",
             "A soma de todos os valores dividida pela quantidade. É sensível a valores extremos: um município com "
             "valor muito alto puxa a média para cima."),
            ("Mediana",
             "O valor do meio quando a lista está em ordem: metade dos municípios fica abaixo e metade acima. "
             "Valores extremos quase não mexem nela."),
            ("Variância",
             "Mede o quanto os valores se espalham em torno da média (é a média dos quadrados das distâncias até a "
             "média). Na população, dividimos por N e chamamos de σ². Na amostra, dividimos por n − 1 e chamamos "
             "de s², o que corrige a tendência da amostra de mostrar menos variação do que existe."),
            ("Desvio padrão",
             "A raiz quadrada da variância. Fica na mesma unidade dos dados, então é mais fácil de interpretar: no "
             "salário do RN, a distância típica de um município até a média é de uns 0,31 salário mínimo."),
            ("Mínimo e máximo",
             "O menor e o maior valor. A distância entre eles é a amplitude."),
            ("Quartis (Q1 e Q3)",
             "Dividem a lista ordenada em quatro partes. Q1 deixa 25% dos municípios abaixo dele, e Q3 deixa 75%. "
             "Quando o quartil cai entre dois valores, ele é calculado por interpolação. Por isso aparece 1,62 no "
             "salário (o valor exato é 1,625), um valor que nenhum município tem."),
            ("Dispersão",
             "O quanto os valores variam de um município para outro. Mede-se pela variância, pelo desvio padrão e "
             "pela distância entre os quartis."),
            ("Assimetria",
             "Diz para que lado a distribuição tem a cauda mais longa. Cauda à direita: poucos valores bem altos, "
             "e o máximo fica bem mais longe de Q3 do que o mínimo fica de Q1. Cauda à esquerda: poucos valores bem "
             "baixos, e a média tende a ficar abaixo da mediana."),
            ("Moda",
             "O valor que mais se repete. Para variáveis contínuas ela não faz sentido, porque, medindo com "
             "precisão, quase nenhum valor se repete. Os empates que aparecem nos dados vêm só do arredondamento "
             "do IBGE para uma casa decimal."),
        ],
        "numeros": [
            ("IDEB, média", "População: PB 5,34 e RN 4,84. Amostra: PB 5,57 e RN 4,85."),
            ("Renda, média (população)", "PB 50,53% e RN 49,10%"),
            ("Salário, média (população)", "PB 1,80 SM e RN 1,83 SM"),
            ("IDEB, desvio padrão (população)", "PB 0,82 e RN 0,66"),
            ("Salário, desvio padrão (população)", "PB 0,23 e RN 0,31"),
            ("Renda do RN, mínimo a máximo", "Amostra: 37,5% a 52,9%. População: 35,5% a 61,4%."),
            ("Maior IDEB da PB", "Coxixola, 8,2 (caiu na amostra)"),
        ],
        "perguntas": [
            ("Por que a variância da população divide por N e a da amostra por n − 1?",
             "Na população temos todos os municípios, então a variância calculada é o valor real (σ²). Na amostra, "
             "as distâncias são medidas até a média da própria amostra, que fica no meio dos dados, e isso faz a "
             "variação parecer um pouco menor do que é. Dividir por n − 1 corrige essa tendência."),
            ("Por que vocês não calcularam a moda?",
             "As três variáveis são quantitativas contínuas, e o próprio enunciado diz que nesse caso a moda não "
             "faz sentido. Se a professora insistir: os valores mais repetidos são 4,7 no IDEB da PB (17 municípios "
             "na população) e 1,8 SM no salário (53 municípios na PB e 29 no RN), mas isso só acontece por causa "
             "do arredondamento."),
            ("Por que o Q1 do salário é 1,62 se nenhum município tem esse valor?",
             "O quartil é calculado por interpolação entre dois valores da lista ordenada, e o valor exato é 1,625. "
             "É o mesmo método do R e do Excel. No cartaz, arredondamos para 1,62 pela regra da ABNT, que manda o "
             "5 final para o algarismo par."),
            ("Por que a média do IDEB na amostra da PB ficou acima da população?",
             "É a variação natural do sorteio: a amostra pegou vários municípios de IDEB alto (Coxixola 8,2, "
             "Cabaceiras 7,7, Cubati 7,1). Mesmo assim, o intervalo de confiança da média (5,19 a 5,95) contém o "
             "valor real, 5,34."),
            ("Como vocês sabem que a renda tem cauda à esquerda?",
             "Nas duas populações, a média fica abaixo da mediana (PB 50,53 contra 50,80; RN 49,10 contra 50,00), e "
             "o coeficiente de assimetria é negativo (cerca de −0,76). Isso vem de poucos municípios com "
             "porcentagem bem baixa, como Várzea, na PB (35,7%), e Parnamirim, no RN (35,5%). Na amostra da PB, a "
             "renda ficou quase simétrica."),
            ("Qual estado é mais desigual?",
             "Depende da variável. No salário, o RN varia mais (desvio padrão 0,31 contra 0,23). No IDEB, a PB varia "
             "mais (0,82 contra 0,66)."),
        ],
    },
    {
        "tema": "Gráficos do salário e intervalo de confiança",
        "curto": "gráficos do salário e intervalo de confiança",
        "quadrante": "inferior esquerdo",
        "fala": [
            ("Aponte para o gráfico azul, da Paraíba.",
             "Aqui está a análise gráfica do salário médio mensal dos trabalhadores formais nas duas amostras. Em "
             "cada gráfico, as barras formam o histograma: cada barra mostra quantos municípios têm salário naquela "
             "faixa de 0,2 salário mínimo. Embaixo fica o boxplot: a caixa vai do primeiro ao terceiro quartil, a "
             "linha dentro dela é a mediana, e o losango é a média."),
            ("Aponte para as duas barras mais altas da PB, com 11 e 13.",
             "A Paraíba é bem concentrada: 24 dos 30 municípios estão de 1,6 a 1,9 salário mínimo, nessas duas "
             "barras do meio."),
            ("Aponte para o gráfico laranja, do RN.",
             "O Rio Grande do Norte é mais espalhado: vai de 1,4 a 2,9 salários mínimos, e a caixa do boxplot é "
             "mais larga."),
            ("Aponte para os pontos isolados à direita, com os nomes dos municípios.",
             "Os dois têm cauda à direita: a maioria dos municípios fica no meio, e poucos têm salário bem mais "
             "alto. Cada amostra tem um valor atípico: Carrapateira, na Paraíba, com 2,4 salários mínimos, e "
             "Riachuelo, no RN, com 2,9. Eles são atípicos porque passam do limite do boxplot, que é o terceiro "
             "quartil mais 1,5 vez a distância entre os quartis."),
            ("Aponte para o gráfico da seção 5.1.",
             "Agora a inferência. Calculamos o intervalo de confiança de 95% para a proporção da população com "
             "renda de até meio salário mínimo. Na Paraíba, a estimativa é 51%, e o intervalo vai de 33,1% a "
             "68,9%. No RN, a estimativa é 48,9%, e o intervalo vai de 31,0% a 66,8%."),
            ("Aponte para os triângulos pretos e passe a palavra.",
             "Como conhecemos a população, conferimos o resultado: o valor real, que é o triângulo, ficou dentro "
             "dos dois intervalos. Os intervalos são largos, de mais ou menos 17,9 pontos percentuais, porque a "
             "amostra tem só 30 municípios. E eles se sobrepõem quase por inteiro, o que já sugere que os dois "
             "estados são parecidos nesse indicador. Agora, {p4} vai mostrar os testes de hipóteses."),
        ],
        "conceitos": [
            ("Histograma",
             "Gráfico de barras para uma variável numérica. O eixo de baixo mostra as faixas de valores (aqui, de "
             "0,2 em 0,2 salário mínimo), e a altura de cada barra mostra quantos municípios caem na faixa. Cada "
             "faixa inclui o valor inicial e vai até antes do final: a barra de 1,6 a 1,8 conta os municípios com "
             "1,6 e 1,7."),
            ("Boxplot",
             "Resume a distribuição em cinco números. A caixa vai de Q1 a Q3 e guarda os 50% centrais, a linha é a "
             "mediana, os bigodes vão até o menor e o maior valor que não são atípicos, e os pontos soltos são os "
             "valores atípicos. Neste cartaz, o losango marca a média."),
            ("AIQ (amplitude interquartil)",
             "Q3 menos Q1, ou seja, o tamanho da caixa. Mede a dispersão dos 50% centrais e não é afetada pelos "
             "extremos. PB: 0,275 SM. RN: 0,375 SM."),
            ("Valor atípico",
             "Valor muito afastado dos demais. A regra do boxplot considera atípico o que fica acima de "
             "Q3 + 1,5 × AIQ ou abaixo de Q1 − 1,5 × AIQ. O limite de cima é 2,31 SM na PB e 2,56 SM no RN."),
            ("Cauda à direita",
             "No histograma, as barras se estendem mais para a direita, com poucas barras baixas longe do centro. "
             "No boxplot, o bigode da direita e os atípicos ficam mais longe da caixa."),
            ("Proporção estimada (p̂, “p chapéu”)",
             "A média das proporções dos 30 municípios sorteados: 51,0% na PB e 48,9% no RN."),
            ("Intervalo de confiança de 95%",
             "Faixa calculada pela fórmula p̂ ± 1,96 × √(p̂(1 − p̂)/n). Ter 95% de confiança quer dizer que, se "
             "repetíssemos o sorteio muitas vezes, cerca de 95% dos intervalos calculados assim conteriam o valor "
             "real."),
            ("Margem de erro",
             "O pedaço que somamos e subtraímos da estimativa: 1,96 vez o erro padrão. Aqui deu 17,9 pontos "
             "percentuais, porque 30 municípios é pouco para essa fórmula."),
            ("Ponto percentual (p.p.)",
             "A diferença entre duas porcentagens. De 51,0% para 33,1% são 17,9 pontos percentuais."),
            ("Valor real",
             "A média das proporções de todos os municípios do estado: 50,5% na PB e 49,1% no RN. Só dá para "
             "conferir porque temos a população inteira."),
        ],
        "numeros": [
            ("Salário da amostra, PB", "1,3 a 2,4 SM. Desvio padrão 0,20. AIQ 0,275."),
            ("Salário da amostra, RN", "1,4 a 2,9 SM. Desvio padrão 0,30. AIQ 0,375."),
            ("Concentração na PB", "24 dos 30 municípios de 1,6 a 1,9 SM"),
            ("Valores atípicos", "Carrapateira (PB), 2,4 SM, limite 2,31. Riachuelo (RN), 2,9 SM, limite 2,56."),
            ("IC da proporção, PB", "51,0%, de 33,1% a 68,9%. Valor real: 50,5%."),
            ("IC da proporção, RN", "48,9%, de 31,0% a 66,8%. Valor real: 49,1%."),
            ("Margem de erro", "±17,9 pontos percentuais"),
        ],
        "perguntas": [
            ("O que quer dizer “95% de confiança”?",
             "Que o método acerta em 95% das amostras possíveis: se repetíssemos o sorteio muitas vezes, cerca de "
             "95% dos intervalos conteriam o valor real. No nosso caso, conferimos, e os dois acertaram."),
            ("Por que o intervalo é tão largo?",
             "A fórmula da proporção trata cada um dos 30 municípios como um único “sim ou não”. Com proporção "
             "perto de 50% e só 30 observações, a margem fica grande. Na prática, as proporções dos municípios "
             "variam bem menos (desvio padrão de uns 3,6 pontos percentuais). Se a renda fosse tratada como uma "
             "média, pelo teste t, o intervalo ficaria com cerca de 1,3 ponto para cada lado, e a diferença entre "
             "os estados daria significativa (p-valor 0,023). Usamos a fórmula de proporção porque é a que a "
             "questão pede."),
            ("Como vocês calcularam a proporção de cada estado?",
             "Pela média das proporções dos 30 municípios sorteados. Como as planilhas não trazem o número de "
             "habitantes, cada município pesa igual."),
            ("Por que Carrapateira e Riachuelo são atípicos?",
             "Pela regra do boxplot: o salário deles passa do limite de cima (Q3 + 1,5 × AIQ), que é 2,31 SM na "
             "PB e 2,56 SM no RN. Os dados não dizem a causa; em município pequeno, poucos empregadores bastam "
             "para mudar a média."),
            ("O que é o losango no boxplot?",
             "A média. Ela fica um pouco abaixo da mediana nos dois estados (PB 1,78 e 1,80; RN 1,88 e 1,90), "
             "porque no meio da distribuição os valores se espalham um pouco mais para baixo. A cauda longa, "
             "porém, é a da direita."),
            ("Por que usar z (a distribuição normal) no intervalo da proporção?",
             "Porque, quando n × p̂ e n × (1 − p̂) passam de 5 (aqui, cerca de 15), a proporção da amostra tem "
             "distribuição aproximadamente normal."),
        ],
    },
    {
        "tema": "Testes de hipóteses e conclusão",
        "curto": "testes de hipóteses e conclusão",
        "quadrante": "inferior direito",
        "fala": [
            ("Aponte para o título 5.2.",
             "Para comparar os estados de forma estatística, usamos testes de hipóteses com nível de "
             "significância de 5%. Em todos os testes, a hipótese nula, H zero, diz que não há diferença entre "
             "Paraíba e Rio Grande do Norte, e a hipótese alternativa diz que há. Quando o p-valor fica abaixo de "
             "0,05, rejeitamos H zero."),
            ("Aponte para a primeira linha da tabela, das proporções.",
             "Na proporção da população com renda de até meio salário mínimo, o teste z para duas proporções deu "
             "p-valor de 0,868, bem acima de 0,05. Então não há diferença significativa, como {p3} já tinha "
             "adiantado pelos intervalos."),
            ("Aponte para as duas linhas do IDEB.",
             "Para comparar médias, seguimos a dica do enunciado: primeiro o teste F compara as variâncias, porque "
             "o resultado decide qual teste t usar. No IDEB, o F deu p-valor de 0,303, então consideramos as "
             "variâncias iguais e usamos o teste t com variância combinada. Ele deu p-valor de 0,004, e rejeitamos "
             "H zero: a média do IDEB da Paraíba é maior, com diferença de 0,72 ponto."),
            ("Aponte para as duas linhas do salário.",
             "No salário, o teste F deu p-valor de 0,026, então as variâncias são diferentes, e usamos o teste t de "
             "Welch, que é a versão para variâncias diferentes. Ele deu p-valor de 0,126, e não rejeitamos H zero: "
             "não há diferença significativa no salário."),
            ("Aponte para a seção 6, Conclusão.",
             "Concluindo: a educação separa os estados, com a Paraíba à frente no IDEB. Renda e salário são "
             "parecidos: cerca de metade da população tem renda de até meio salário mínimo, e o salário formal "
             "fica perto de 1,8 salário mínimo. O RN é mais heterogêneo no salário. E as amostras representaram "
             "bem as populações, porque todos os intervalos de confiança contêm os valores reais."),
            ("Olhe para a professora para fechar.",
             "Na prática, como renda e salário são parecidos, a vantagem da Paraíba no IDEB não parece vir dessas "
             "variáveis, e vale investigar a gestão e as políticas educacionais. Agradecemos a atenção e estamos "
             "abertos a perguntas."),
        ],
        "conceitos": [
            ("Teste de hipóteses",
             "Um método para decidir, com base na amostra, se uma diferença é grande demais para ser só acaso do "
             "sorteio."),
            ("H₀ e H₁",
             "H₀ (hipótese nula) diz que não há diferença: as proporções, as variâncias ou as médias dos dois "
             "estados são iguais. H₁ (hipótese alternativa) diz que há diferença. Usamos H₁ bilateral (≠), porque "
             "não supusemos de antemão qual estado seria maior."),
            ("Nível de significância (α = 5%)",
             "O risco que aceitamos de rejeitar H₀ quando ela é verdadeira, ou seja, de enxergar uma diferença que "
             "não existe."),
            ("p-valor",
             "A probabilidade de aparecer uma diferença tão grande quanto a nossa, ou maior, se H₀ fosse "
             "verdadeira. p-valor abaixo de 0,05 quer dizer que a diferença dificilmente é só acaso, e aí "
             "rejeitamos H₀."),
            ("Rejeitar ou não rejeitar H₀",
             "Rejeitar H₀ é concluir que há diferença. Não rejeitar quer dizer que a amostra não trouxe evidência "
             "de diferença; isso não prova que os estados são iguais."),
            ("Teste z para duas proporções",
             "Compara duas proporções. Mede quantos erros padrão separam as duas estimativas: deu z = 0,17, muito "
             "longe do limite de 1,96."),
            ("Teste F",
             "Compara duas variâncias dividindo uma pela outra (F = s² da PB ÷ s² do RN). Com variâncias iguais, F "
             "fica perto de 1. Com 30 municípios por estado, um F entre 0,476 e 2,101 é compatível com variâncias "
             "iguais."),
            ("Teste t com variância combinada",
             "Compara duas médias supondo variâncias iguais, juntando as duas variâncias numa só. Tem "
             "30 + 30 − 2 = 58 graus de liberdade."),
            ("Teste t de Welch",
             "Compara duas médias sem supor variâncias iguais: usa a variância de cada estado separada. Os graus "
             "de liberdade saem de uma fórmula própria (aqui, cerca de 50)."),
            ("Graus de liberdade (gl)",
             "Número que define a forma exata das distribuições t e F. Depende do tamanho das amostras."),
            ("Intervalo da diferença",
             "No IDEB, a diferença entre as médias (0,72 ponto) tem intervalo de confiança de 95% de 0,24 a 1,20. "
             "Como o intervalo não contém o zero, ele concorda com a rejeição de H₀."),
            ("Shapiro-Wilk e Teorema Central do Limite",
             "O Shapiro-Wilk testa se os dados parecem vir de uma distribuição normal, e apontou desvios em "
             "algumas variáveis. O Teorema Central do Limite diz que, com amostras de 30 ou mais, a média da "
             "amostra tem distribuição aproximadamente normal mesmo assim, e isso sustenta o teste t."),
        ],
        "numeros": [
            ("Proporções (teste z)", "z = 0,17. p-valor 0,868. Não rejeita H₀."),
            ("IDEB, variâncias (F)", "F = 1,47. p-valor 0,303. Variâncias iguais."),
            ("IDEB, médias (t combinado)", "t = 3,02 com 58 gl. p-valor 0,004. Rejeita H₀."),
            ("IDEB, diferença das médias", "0,72 ponto, IC de 95% de 0,24 a 1,20"),
            ("Salário, variâncias (F)", "F = 0,43. p-valor 0,026. Variâncias diferentes."),
            ("Salário, médias (Welch)", "t = −1,56 com cerca de 50 gl. p-valor 0,126. Não rejeita H₀."),
            ("Valores críticos", "z: ±1,96. t com 58 gl: ±2,00. t com 50 gl: ±2,01. F: 0,476 e 2,101."),
        ],
        "perguntas": [
            ("O que é o p-valor?",
             "É a probabilidade de observar uma diferença tão grande quanto a da amostra, ou maior, se H₀ fosse "
             "verdadeira. No IDEB, deu 0,004: se as médias fossem iguais, uma diferença como a nossa apareceria em "
             "só 0,4% das amostras. Por isso rejeitamos H₀."),
            ("Por que fazer o teste F antes do t?",
             "Porque existem dois testes t: um para variâncias iguais e outro, o de Welch, para variâncias "
             "diferentes. O F diz qual suposição usar, como a dica do enunciado pede."),
            ("E se vocês tivessem usado o outro teste t?",
             "A decisão seria a mesma. No IDEB, o de Welch daria p-valor 0,004; no salário, o t com variâncias "
             "iguais daria 0,125."),
            ("Os dados são normais? Dá para usar o teste t?",
             "O teste de Shapiro-Wilk aponta desvios da normal no salário e no IDEB do RN. Com 30 municípios por "
             "estado, o Teorema Central do Limite faz a média da amostra ter distribuição aproximadamente normal, "
             "e o teste t continua válido."),
            ("O teste F é confiável aqui?",
             "Ele é sensível à falta de normalidade. No salário, o teste de Levene, que não depende disso, deu "
             "p-valor 0,097 e não rejeitaria variâncias iguais. Como os dois testes t chegam na mesma conclusão, a "
             "decisão sobre as médias não muda."),
            ("Então as escolas da Paraíba são melhores?",
             "O teste mostra que a média do IDEB dos anos iniciais da rede pública é maior na PB, de 0,24 a 1,20 "
             "ponto a mais. Ele não mostra a causa, e o IDEB mede só essa etapa da rede pública."),
            ("Não rejeitar H₀ prova que os salários são iguais?",
             "Não prova. Quer dizer que a amostra não trouxe evidência suficiente de diferença. O intervalo da "
             "diferença, de −0,24 a 0,03 SM, contém o zero."),
        ],
    },
]

COMUM = [
    "Em uma frase: a Paraíba tem IDEB maior que o Rio Grande do Norte, com diferença significativa, e renda e "
    "salário são parecidos nos dois estados.",
    "As amostras têm 30 municípios por estado, sorteados por amostragem aleatória simples, sem reposição, com "
    "semente fixa (20261116).",
    "Testes com nível de significância de 5%: no IDEB, p-valor 0,004 (há diferença); na renda, 0,868, e no "
    "salário, 0,126 (sem diferença).",
    "Os 6 intervalos de confiança do trabalho (2 de proporção e 4 de média) contêm os valores reais da população.",
    "Se perguntarem algo de outra parte, responda o que souber ou passe para quem apresentou: metodologia com "
    "{p1}, tabela com {p2}, gráficos e intervalos com {p3}, testes e conclusão com {p4}.",
]

DICAS = [
    "Ensaiem juntos pelo menos duas vezes, cronometrando.",
    "Fale olhando para a turma e apontando para o cartaz. Se esquecer um número, olhe para o cartaz: todos "
    "estão lá.",
    "Leia a seção 4 com atenção: a professora pode perguntar para qualquer integrante.",
    "Se não souber uma resposta, diga o que sabe e passe para o colega da parte certa.",
]


# ---------------------------------------------------------------- integrantes
nomes = [n.strip() for n in CFG["integrantes"]]
if len(nomes) != len(PARTES):
    sys.exit(f"O roteiro está dividido em {len(PARTES)} partes, e o config.json tem {len(nomes)} integrantes. "
             "Ajuste a divisão em falas/gerar_falas.py (lista PARTES).")
primeiros = [n.split()[0] for n in nomes]
lista = ", ".join(primeiros[:-1]) + " e " + primeiros[-1]
NOMES = {f"p{i + 1}": p for i, p in enumerate(primeiros)} | {"todos": lista}


def texto(t):
    return html.escape(t.format_map(NOMES))


def segundos_de_fala(parte):
    palavras = sum(len(t.format_map(NOMES).split()) for _, t in parte["fala"])
    return round(palavras / PALAVRAS_POR_MINUTO * 60 / 15) * 15  # arredonda para 15 s


def tempo(segundos):
    minutos, resto = divmod(segundos, 60)
    return f"cerca de {minutos} min" + (f" {resto} s" if resto else "")


# ---------------------------------------------------------------- imagens do cartaz
if not CARTAZ.exists():
    sys.exit("Não achei o cartaz/cartaz_A2.pdf. Rode antes: python cartaz\\montar_cartaz.py")
cartaz = fitz.open(CARTAZ)
pagina = cartaz[0]
L, A = pagina.rect.width, pagina.rect.height
QUADROS = [fitz.Rect(0, 0, L / 2, A / 2), fitz.Rect(L / 2, 0, L, A / 2),
           fitz.Rect(0, A / 2, L / 2, A), fitz.Rect(L / 2, A / 2, L, A)]


def imagem(dpi, clip=None):
    jpeg = pagina.get_pixmap(dpi=dpi, clip=clip).tobytes("jpeg", jpg_quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(jpeg).decode()


miniatura = imagem(32)

# ---------------------------------------------------------------- montagem das páginas
navegador = next((p for p in NAVEGADORES if p.exists()), None)
if navegador is None:
    sys.exit("Não achei Chrome nem Edge para gerar os PDFs.")

modelo = Template((PASTA / "modelo_falas.html").read_text(encoding="utf-8"))
tempos = [segundos_de_fala(p) for p in PARTES]  # o total é a soma das partes já arredondadas
for antigo in PASTA.glob("falas (*).pdf"):  # nomes trocados no config.json não deixam PDF velho para trás
    antigo.unlink()

with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    for i, (nome, parte) in enumerate(zip(nomes, PARTES)):
        mapa = "".join(f'<span class="q q{k + 1}{" voce" if k == i else ""}"><b>{k + 1}</b></span>'
                       for k in range(len(PARTES)))
        destaque = ['class="voce"' if k == i else "" for k in range(len(PARTES))]
        ordem = "".join(
            f'<li {destaque[k]}><span class="n">{k + 1}</span>'
            f'<span><b>{html.escape(primeiros[k])}</b> · {html.escape(p["curto"])}</span></li>'
            for k, p in enumerate(PARTES))
        if i == 0:
            entrada = f"Você abre a apresentação. No fim da sua fala, passe a palavra para {primeiros[1]}."
        elif i == len(PARTES) - 1:
            entrada = f"Você fala depois de {primeiros[i - 1]} e fecha a apresentação, abrindo para perguntas."
        else:
            entrada = (f"Você fala depois de {primeiros[i - 1]}. No fim da sua fala, passe a palavra para "
                       f"{primeiros[i + 1]}.")
        fala = "".join(f'<div class="bloco"><p class="gesto">→ {texto(g)}</p><p class="texto">{texto(t)}</p></div>'
                       for g, t in parte["fala"])
        conceitos = "".join(f"<dt>{texto(c)}</dt><dd>{texto(e)}</dd>" for c, e in parte["conceitos"])
        numeros = "".join(f"<tr><th>{texto(r)}</th><td>{texto(v)}</td></tr>" for r, v in parte["numeros"])
        perguntas = "".join(f'<div class="pergunta"><p class="p">“{texto(p)}”</p><p class="r">{texto(r)}</p></div>'
                            for p, r in parte["perguntas"])
        pagina_html = modelo.substitute(
            nome=html.escape(nome), parte=i + 1, total_partes=len(PARTES), tema=html.escape(parte["tema"]),
            quadrante=parte["quadrante"], miniatura=miniatura, mapa=mapa, ordem=ordem,
            tempo=tempo(tempos[i]), tempo_total=tempo(sum(tempos)), entrada=html.escape(entrada),
            fala=fala, conceitos=conceitos, numeros=numeros, perguntas=perguntas,
            comum="".join(f"<li>{texto(c)}</li>" for c in COMUM),
            dicas="".join(f"<li>{texto(d)}</li>" for d in DICAS),
            quadro=imagem(150, QUADROS[i]))
        arq_html = temp / f"falas_{i + 1}.html"
        arq_html.write_text(pagina_html, encoding="utf-8")
        arq_pdf = PASTA / f"falas ({nome}).pdf"
        subprocess.run([str(navegador), "--headless=new", "--disable-gpu", f"--user-data-dir={temp / 'perfil'}",
                        "--no-pdf-header-footer", "--print-to-pdf-no-header", f"--print-to-pdf={arq_pdf}",
                        arq_html.as_uri()], capture_output=True, timeout=120, check=True)
        paginas = len(fitz.open(arq_pdf))
        print(f"{arq_pdf.name}: parte {i + 1}, {paginas} páginas, fala de {tempo(tempos[i])}")
