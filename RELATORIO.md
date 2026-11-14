# Projeto da Unidade II: IDEB, renda e salário (PB × RN)

Métodos Estatísticos Aplicados às Ciências Tecnológicas (UFPB) · Docente: Renilma Pereira · Valor: 4,0 pontos · Apresentação: segunda, 16/11/2026

Este arquivo tem as respostas completas das 5 questões, as escolhas de método (com o porquê), o roteiro da apresentação, as perguntas que a professora pode fazer e o passo a passo para preencher, gerar de novo e imprimir o cartaz. O cartaz traz a versão resumida de tudo isso.

Todos os caminhos abaixo partem da pasta `projeto-un2`.

---

## 1. O que está pronto

| Arquivo | Para que serve |
|---|---|
| `cartaz/cartaz_A2.pdf` | O cartaz inteiro em 1 página A2 (42 × 59,4 cm). Para gráfica. Como é vetorial, amplia para A1 sem perder qualidade. |
| `cartaz/cartaz_4xA4.pdf` | O mesmo cartaz em 4 folhas A4, para imprimir em casa e colar 2 × 2 na cartolina. |
| `cartaz/cartaz_2xA3.pdf` | O mesmo cartaz em 2 folhas A3 deitadas, para copiadora. |
| `cartaz/cartaz.html` | Versão de tela, abre no navegador. É gerado pelo script, então não adianta editar à mão. |
| `dados/amostras.xlsx` | As planilhas das amostras: abas "Amostra 1 - PB", "Amostra 2 - RN" e "Sobre os dados". Este é o arquivo que vai para o Google Drive. |
| `saida/resultados.json` | Todos os números calculados. O cartaz lê daqui. |
| `saida/graficos/` | Os 3 gráficos em SVG e PNG, caso alguém queira usar em slide. |
| `analise/analise.py` | Sorteia as amostras e faz todas as contas. |
| `cartaz/montar_cartaz.py`, `cartaz/modelo.html`, `cartaz/config.json` | Montam o cartaz. Grupo, nomes e link ficam no `config.json`. |
| `falas/falas (Nome).pdf` | Um PDF por integrante, em A5: a fala com as indicações de onde apontar, a explicação de cada conceito, os números e as perguntas prováveis da sua parte. |
| `falas/gerar_falas.py`, `falas/modelo_falas.html` | Geram os PDFs de falas a partir dos nomes do `config.json` e do cartaz pronto. |

Falta 1 coisa: liberar a pasta do Google Drive para "Qualquer pessoa com o link". Em 14/11/2026, quem abria o link sem login caía na tela de login do Google, então a professora não conseguiria abrir a planilha pelo QR code. A seção 8.1 mostra como liberar; o link e o QR code do cartaz continuam os mesmos.

---

## 2. Como as amostras foram sorteadas

- **Tipo de amostragem:** aleatória simples (AAS: todo município tem a mesma chance de sair), sem reposição (um município não sai duas vezes), com n = 30 por estado.
- **Sorteio por computador com semente 20261116.** A semente é o número que fixa a sequência "aleatória" do computador: quem rodar o script de novo obtém exatamente os mesmos 30 municípios. A PB foi sorteada primeiro, depois o RN, com o mesmo gerador.
- **Base de sorteio:** 6 municípios de cada estado não têm IDEB divulgado (aparecem com "-" na planilha do IBGE). Como cada município da amostra precisa ter as 3 variáveis, eles ficaram fora do sorteio.
  - PB, 223 → 217: Baía da Traição, Barra de Santa Rosa, Santana dos Garrotes, São José de Princesa, São José do Brejo do Cruz, Vista Serrana.
  - RN, 167 → 161: Água Nova, Jardim de Angicos, Paraú, Pedra Grande, São Fernando, Serra Negra do Norte.
  - O efeito é desprezível: a média da renda na base de 217 municípios é 50,47%, contra 50,53% nos 223; no RN, 49,06% contra 49,10%. O salário muda menos de 0,01 SM.
- A planilha lista os municípios em ordem alfabética, e a coluna "Ordem no sorteio" mostra em que ordem cada um saiu.

**Amostra 1 (PB):** Barra de São Miguel, Bernardino Batista, Bom Jesus, Bonito de Santa Fé, Boqueirão, Cabaceiras, Camalaú, Carrapateira, Congo, Coremas, Coxixola, Cubati, Frei Martinho, Gurinhém, Itapororoca, Jacaraú, Juarez Távora, Lastro, Maturéia, Pedro Régis, Riachão do Bacamarte, Santana de Mangueira, São Domingos, São José dos Cordeiros, São Sebastião do Umbuzeiro, Serra Grande, Tacima, Teixeira, Tenório, Uiraúna.

**Amostra 2 (RN):** Acari, Açu, Afonso Bezerra, Alto do Rodrigues, Baraúna, Bento Fernandes, Caiçara do Rio do Vento, Coronel Ezequiel, Coronel João Pessoa, Encanto, Ipueira, João Câmara, José da Penha, Monte das Gameleiras, Passa e Fica, Pedro Velho, Pendências, Pilões, Riacho da Cruz, Riachuelo, Ruy Barbosa, Santa Cruz, São Francisco do Oeste, São Tomé, Serra Caiada, Sítio Novo, Taipu, Tenente Laurentino Cruz, Várzea, Vera Cruz.

---

## 3. Respostas das questões

### Questão 1: estatísticas descritivas

Variância com divisor N na população (σ²) e n − 1 na amostra (s²). CV é o coeficiente de variação (desvio padrão dividido pela média), que permite comparar a dispersão de variáveis com unidades diferentes. Assimetria é o coeficiente de assimetria: positivo indica cauda à direita, negativo indica cauda à esquerda.

**IDEB, anos iniciais do ensino fundamental, rede pública (escala de 0 a 10)**

| | n | Média | Mediana | Variância | Desvio padrão | Mín. | Q1 | Q3 | Máx. | CV | Assimetria |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PB · população | 217 | 5,34 | 5,20 | 0,670 | 0,82 | 3,60 | 4,80 | 5,80 | 8,20 | 15,3% | 0,73 |
| PB · amostra | 30 | 5,57 | 5,45 | 1,015 | 1,01 | 3,90 | 4,92 | 6,10 | 8,20 | 18,1% | 0,86 |
| RN · população | 161 | 4,84 | 4,80 | 0,440 | 0,66 | 3,60 | 4,40 | 5,20 | 7,60 | 13,7% | 0,78 |
| RN · amostra | 30 | 4,85 | 4,70 | 0,689 | 0,83 | 3,60 | 4,30 | 5,20 | 7,60 | 17,1% | 1,40 |

**Renda: % da população com rendimento per capita de até 1/2 salário mínimo**

| | n | Média | Mediana | Variância | Desvio padrão | Mín. | Q1 | Q3 | Máx. | CV | Assimetria |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PB · população | 223 | 50,53 | 50,80 | 13,58 | 3,68 | 35,70 | 48,60 | 53,00 | 60,40 | 7,3% | −0,76 |
| PB · amostra | 30 | 51,01 | 51,30 | 12,85 | 3,59 | 44,00 | 48,62 | 52,50 | 60,40 | 7,0% | 0,30 |
| RN · população | 167 | 49,10 | 50,00 | 19,36 | 4,40 | 35,50 | 47,25 | 51,95 | 61,40 | 9,0% | −0,77 |
| RN · amostra | 30 | 48,87 | 50,00 | 12,35 | 3,51 | 37,50 | 47,40 | 51,50 | 52,90 | 7,2% | −1,38 |

**Salário médio mensal dos trabalhadores formais (em salários mínimos, SM)**

| | n | Média | Mediana | Variância | Desvio padrão | Mín. | Q1 | Q3 | Máx. | CV | Assimetria |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PB · população | 223 | 1,80 | 1,80 | 0,051 | 0,23 | 1,20 | 1,60 | 1,90 | 2,70 | 12,6% | 0,99 |
| PB · amostra | 30 | 1,78 | 1,80 | 0,040 | 0,20 | 1,30 | 1,62 | 1,90 | 2,40 | 11,2% | 0,57 |
| RN · população | 167 | 1,83 | 1,80 | 0,094 | 0,31 | 1,20 | 1,60 | 2,00 | 3,30 | 16,8% | 1,27 |
| RN · amostra | 30 | 1,88 | 1,90 | 0,093 | 0,30 | 1,40 | 1,62 | 2,00 | 2,90 | 16,2% | 1,12 |

**Moda: não se aplica.** As três variáveis são quantitativas contínuas, e o próprio enunciado observa que não faz sentido calcular a moda nesse caso. Os valores repetidos que aparecem nos dados vêm só do arredondamento do IBGE para uma casa decimal.

**População × amostra**

- *Tendência central:* as médias e medianas das amostras ficaram perto das populacionais. A maior distância relativa é o IDEB da PB (5,57 na amostra contra 5,34 na população, cerca de 4% da média). A amostra da PB pegou vários municípios de IDEB alto: Coxixola (8,2, o máximo do estado), Cabaceiras (7,7) e Cubati (7,1). Em valor absoluto, a renda da PB se afasta um pouco mais (51,01% contra 50,53%), mas isso representa menos de 1% da média.
- *Dispersão:* a variância da amostra oscila em torno da populacional. No IDEB, as duas amostras ficaram mais dispersas que as populações (PB 1,015 contra 0,670; RN 0,689 contra 0,440), porque pegaram valores extremos: a amostra do RN contém o mínimo (Bento Fernandes, 3,6) e o máximo (Ipueira, 7,6) do estado. Na renda do RN acontece o contrário: a amostra ficou menos dispersa (12,35 contra 19,36), porque não pegou os extremos (37,5% a 52,9% na amostra, contra 35,5% a 61,4% na população). No salário, as variâncias quase coincidem.
- *Extremos:* o intervalo de valores da amostra fica dentro do da população e costuma ser mais estreito, já que é raro sortear justamente os municípios mais extremos.

**Paraíba × Rio Grande do Norte**

- *IDEB:* maior na PB, tanto na população (média 5,34 contra 4,84; mediana 5,2 contra 4,8) quanto na amostra (5,57 contra 4,85).
- *Renda:* centros parecidos, perto de 50% (populações: 50,53% na PB e 49,10% no RN; medianas 50,8% e 50,0%). Ou seja, em um município típico dos dois estados, cerca de metade da população tem renda per capita de até 1/2 SM.
- *Salário:* centros parecidos, perto de 1,8 SM (médias 1,80 e 1,83; medianas iguais, 1,8).
- *Dispersão (nas populações):* a PB varia mais no IDEB (desvio padrão 0,82 contra 0,66), e o RN varia mais na renda (4,40 contra 3,68) e no salário (0,31 contra 0,23; CV 16,8% contra 12,6%). Pelo CV, a renda é a variável mais homogênea (7% a 9%), e IDEB e salário variam mais (11% a 18%).
- *Assimetria:* IDEB e salário têm cauda à direita nos dois estados, com poucos municípios de valor bem alto. No IDEB, Coxixola (8,2) na PB e Ipueira (7,6) no RN; no salário, Guamaré (3,3 SM) no RN e João Pessoa, São José de Caiana e São José do Bonfim (2,7 SM) na PB. Nesses casos, o máximo fica bem mais longe de Q3 do que o mínimo fica de Q1. A renda tem cauda à esquerda nas duas populações (média abaixo da mediana), com poucos municípios de proporção bem menor que a dos demais: Várzea, na PB (35,7%), e Parnamirim, no RN (35,5%). Nas amostras, a renda do RN repete a cauda à esquerda (−1,38, puxada por Ipueira, 37,5%), e a da PB fica quase simétrica (+0,30): a média ainda fica um pouco abaixo da mediana, mas o maior valor (Santana de Mangueira, 60,4%) puxa a cauda direita.

Observação: existe um município chamado Várzea em cada estado. O Várzea da renda mínima acima é o da PB; o Várzea da Amostra 2 é o do RN.

### Questão 2: histogramas e boxplots do salário

O gráfico do quadrante 3 tem, para cada amostra, um histograma (classes de 0,2 SM, fechadas à esquerda: [1,6; 1,8) inclui 1,6 e 1,7) e um boxplot horizontal. No boxplot, a caixa vai de Q1 a Q3, a linha é a mediana, o losango é a média, e os bigodes vão até o último valor dentro dos limites Q1 − 1,5·AIQ e Q3 + 1,5·AIQ, onde AIQ = Q3 − Q1 (amplitude interquartil). Fora desses limites, o ponto é um valor atípico.

| Classe (SM) | [1,2; 1,4) | [1,4; 1,6) | [1,6; 1,8) | [1,8; 2,0) | [2,0; 2,2) | [2,2; 2,4) | [2,4; 2,6) | [2,6; 2,8) | [2,8; 3,0) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PB (municípios) | 1 | 1 | 11 | 13 | 3 | 0 | 1 | 0 | 0 |
| RN (municípios) | 0 | 3 | 6 | 9 | 9 | 2 | 0 | 0 | 1 |

| | Mín. | Q1 | Mediana | Q3 | Máx. | AIQ | Limite inferior | Limite superior | Atípicos |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PB | 1,3 | 1,625 | 1,8 | 1,9 | 2,4 | 0,275 | 1,21 | 2,31 | Carrapateira (2,4) |
| RN | 1,4 | 1,625 | 1,9 | 2,0 | 2,9 | 0,375 | 1,06 | 2,56 | Riachuelo (2,9) |

- **Dispersão:** o RN é mais disperso. Amplitude de 1,5 SM (1,4 a 2,9) contra 1,1 SM na PB (1,3 a 2,4); desvio padrão 0,30 contra 0,20; AIQ 0,375 contra 0,275. A PB é concentrada: 24 dos 30 municípios estão de 1,6 a 1,9 SM (as duas barras centrais do histograma). No RN, essas mesmas barras têm 15 municípios, e o resto se espalha de 1,4 até 2,9.
- **Assimetria:** no meio da distribuição, os dados se espalham um pouco mais abaixo da mediana (a metade esquerda da caixa é mais longa, e a média fica 0,02 SM abaixo da mediana nos dois estados). Já a cauda direita é bem mais longa que a esquerda, por causa dos poucos municípios de salário alto. O coeficiente de assimetria, que dá mais peso aos extremos, é positivo nos dois (PB 0,57; RN 1,12), e a cauda direita é mais longa no RN.
- **Valores atípicos:** um em cada amostra, os dois acima do limite superior: Carrapateira (PB, 2,4 SM, limite 2,31) e Riachuelo (RN, 2,9 SM, limite 2,56). Não há atípico inferior. O do RN fica mais longe do resto dos dados. Os dados não explicam a causa; em município pequeno, poucos empregadores (a prefeitura ou uma única empresa) bastam para mudar a média.
- **Comparação:** os dois estados têm centro parecido (medianas 1,8 e 1,9 SM), mas o salário formal é mais homogêneo na PB e mais desigual entre municípios no RN.

### Questão 3: IC de 95% para a proporção e teste de diferença de proporções

**Estimativa:** a proporção de cada amostra (p̂, lê-se "p chapéu") é a média das 30 proporções municipais da variável renda: p̂_PB = 0,5101 (51,0%) e p̂_RN = 0,4887 (48,9%).

**Intervalo de confiança (IC):** p̂ ± z·√(p̂(1 − p̂)/n), com z = 1,96 (95%) e n = 30.

| | p̂ | Erro padrão | Margem de erro | IC de 95% | Valor real (média de todos os municípios) | Contém? |
|---|---:|---:|---:|---|---:|---|
| PB | 51,0% | 0,0913 | ±17,9 p.p. | 33,1% a 68,9% | 50,5% | sim |
| RN | 48,9% | 0,0913 | ±17,9 p.p. | 31,0% a 66,8% | 49,1% | sim |

Conta da PB: √(0,5101 × 0,4899 / 30) = 0,0913; 1,96 × 0,0913 = 0,179; 0,510 ± 0,179.

*Interpretação:* com 95% de confiança, a proporção da população com renda per capita de até 1/2 SM está entre 33,1% e 68,9% na PB e entre 31,0% e 66,8% no RN. "95% de confiança" quer dizer que, se o sorteio fosse repetido muitas vezes, cerca de 95% dos intervalos calculados desse jeito conteriam o valor real. Aqui dá para conferir, porque a população é conhecida: os dois intervalos acertaram. Os intervalos se sobrepõem quase por inteiro, e a margem é larga (±17,9 pontos percentuais) porque n = 30 é pequeno para essa fórmula.

**Teste de hipóteses (teste z para duas proporções):**

- H₀: p_PB = p_RN (as proporções são iguais) · H₁: p_PB ≠ p_RN (bilateral) · α = 5%.
- Proporção combinada: p̄ = (30 × 0,5101 + 30 × 0,4887) / 60 = 0,4994.
- Erro padrão: √(0,4994 × 0,5006 × (1/30 + 1/30)) = 0,1291.
- z = (0,5101 − 0,4887) / 0,1291 = 0,17. Valores críticos: ±1,96. p-valor = 0,868.
- **Decisão:** como |z| < 1,96 (ou p-valor > 0,05), não se rejeita H₀.
- **Conclusão:** ao nível de 5%, não há evidência de diferença entre as proporções da PB e do RN. Nos dois estados, a proporção fica perto de 50%.

### Questão 4: médias do IDEB (α = 5%)

**Passo 1, suposição sobre as variâncias (teste F):**

- H₀: σ²_PB = σ²_RN · H₁: σ²_PB ≠ σ²_RN.
- F = s²_PB / s²_RN = 1,0153 / 0,6895 = 1,47, com 29 e 29 graus de liberdade (gl).
- Região de não rejeição: de 0,476 a 2,101. p-valor = 0,303.
- **Decisão:** não se rejeita H₀. Suposição adotada: variâncias populacionais iguais (homocedasticidade).

**Passo 2, comparação das médias (teste t com variância combinada):**

- H₀: μ_PB = μ_RN · H₁: μ_PB ≠ μ_RN.
- Variância combinada: s²_p = (29 × 1,0153 + 29 × 0,6895) / 58 = 0,8524.
- Erro padrão: √(0,8524 × (1/30 + 1/30)) = 0,2384.
- t = (5,57 − 4,85) / 0,2384 = 3,02, com 58 gl. Valores críticos: ±2,00. p-valor = 0,004.
- **Decisão:** rejeita-se H₀.
- **Interpretação:** a média do IDEB dos anos iniciais é significativamente maior na PB. A diferença estimada é de 0,72 ponto, e o IC de 95% da diferença vai de 0,24 a 1,20 ponto (não contém o zero). A população confirma: 5,34 na PB contra 4,84 no RN.
- **Robustez:** o teste t de Welch (sem supor variâncias iguais) dá o mesmo resultado (t = 3,02; 56 gl; p-valor = 0,004), e o teste de Levene (alternativa ao F que não depende de normalidade) também não rejeita variâncias iguais (p-valor = 0,39).

### Questão 5: médias do salário (α = 5%)

**Passo 1, teste F:**

- H₀: σ²_PB = σ²_RN · H₁: σ²_PB ≠ σ²_RN.
- F = 0,0398 / 0,0927 = 0,43, com 29 e 29 gl. Fica abaixo de 0,476, o limite inferior da região de não rejeição. p-valor = 0,026.
- **Decisão:** rejeita-se H₀. Suposição adotada: variâncias diferentes (heterocedasticidade), com o RN mais disperso.

**Passo 2, teste t de Welch (para variâncias diferentes):**

- H₀: μ_PB = μ_RN · H₁: μ_PB ≠ μ_RN.
- Erro padrão: √(0,0398/30 + 0,0927/30) = 0,0665.
- t = (1,7767 − 1,8800) / 0,06645 = −1,56, com cerca de 50 gl (fórmula de Welch-Satterthwaite). Valores críticos: ±2,01. p-valor = 0,126.
- **Decisão:** não se rejeita H₀.
- **Interpretação:** não há evidência de diferença entre os salários médios dos dois estados; os dois ficam perto de 1,8 SM. O IC de 95% da diferença (PB − RN) vai de −0,24 a 0,03 SM e contém o zero. A população confirma: 1,80 contra 1,83.
- **Robustez:** com o t de variâncias iguais, o p-valor seria 0,125, a mesma decisão. O teste de Levene não rejeitaria a igualdade das variâncias (p-valor = 0,097), mas, como os dois testes t concordam, a conclusão sobre as médias não depende dessa escolha.

### Complemento: IC de 95% das médias (gráfico do quadrante 4)

Fórmula: x̄ ± t·s/√n, com t = 2,045 (29 gl), porque o desvio padrão da população é tratado como desconhecido.

| | Média da amostra | IC de 95% | Valor real | Contém? |
|---|---:|---|---:|---|
| IDEB PB | 5,57 | 5,19 a 5,95 | 5,34 | sim |
| IDEB RN | 4,85 | 4,54 a 5,16 | 4,84 | sim |
| Salário PB | 1,78 | 1,70 a 1,85 | 1,80 | sim |
| Salário RN | 1,88 | 1,77 a 1,99 | 1,83 | sim |

Somando com os 2 ICs da proporção, os 6 intervalos contêm o valor real.

---

## 4. Escolhas de método (e o porquê)

1. **Base de sorteio sem os 6 municípios sem IDEB de cada estado.** A análise usa as 3 variáveis do mesmo município, e o efeito nas médias é desprezível (seção 2).
2. **Variância com N na população e n − 1 na amostra.** Com todos os municípios, a variância é o próprio parâmetro (σ²). Na amostra, dividir por n − 1 corrige o viés da estimativa (s²). O `var()` do R sempre divide por n − 1; por isso, quem calcular a variância da população no R vai achar valores um pouco maiores (IDEB da PB: 0,674 contra 0,670). No Excel, VAR.P divide por N e VAR.A por n − 1.
3. **Quartis pelo método linear (tipo 7).** É o padrão do R (`quantile()` e `summary()`) e do Excel (QUARTIL.INC). Por isso o Q1 do salário dá 1,625, um valor que não aparece nos dados: ele fica entre dois valores da lista.
4. **Moda não calculada,** conforme a observação do próprio enunciado.
5. **Arredondamento pela regra da ABNT NBR 5891:** quando o que sobra é exatamente 5, arredonda-se para o algarismo par (1,625 → 1,62; 4,925 → 4,92; 48,625 → 48,62). O Excel arredondaria 1,625 para 1,63; a diferença está só na última casa.
6. **Proporção = média das 30 proporções municipais, com n = 30.** As planilhas trazem a proporção de cada município, sem o número de habitantes, então cada município pesa igual. O "valor real" usado para conferir é a média de todos os municípios do estado (seção 6, pergunta 5).
7. **Teste F antes do t,** seguindo a dica do enunciado: o F decide a suposição sobre as variâncias. Variâncias iguais levam ao t com variância combinada; diferentes, ao t de Welch.
8. **Normalidade:** o teste de Shapiro-Wilk aponta desvios da normal em algumas variáveis (p-valores: IDEB PB 0,10 e RN 0,010; salário PB 0,048 e RN 0,018). Com n = 30 por estado, o Teorema Central do Limite garante que a média amostral tem distribuição aproximadamente normal, o que sustenta os testes t.
9. **Conferência com o valor real,** a mesma ideia da linha `mu1>=lim_inf & mu1<=lim_sup` do script de exemplo da professora.
10. **Ferramenta:** Python (pandas, SciPy, Matplotlib) no lugar do R. As fórmulas são as mesmas. Os comandos equivalentes no R estão abaixo; eles não foram rodados aqui (o R não está instalado nesta máquina), mas `var.test` e `t.test` usam exatamente as fórmulas acima, então devem dar os mesmos números.

```r
library(readxl)
pb <- read_excel("amostras.xlsx", sheet = "Amostra 1 - PB")
rn <- read_excel("amostras.xlsx", sheet = "Amostra 2 - RN")
# coluna 3 = IDEB, coluna 4 = renda, coluna 5 = salário
var.test(pb[[3]], rn[[3]])                  # IDEB: F = 1,47; p-valor = 0,303
t.test(pb[[3]], rn[[3]], var.equal = TRUE)  # IDEB: t = 3,02; p-valor = 0,004
var.test(pb[[5]], rn[[5]])                  # salário: F = 0,43; p-valor = 0,026
t.test(pb[[5]], rn[[5]])                    # salário (Welch, padrão do R): t = -1,56; p-valor = 0,126
```

---

## 5. Roteiro da apresentação

O enunciado exige que todos participem. A divisão abaixo segue os 4 quadrantes do cartaz e a ordem dos nomes no `config.json`: Augusto (parte 1), Pedro (parte 2), Luy (parte 3) e Luiz (parte 4), uns 8 minutos no total. Cada um tem a versão completa da sua parte em `falas/falas (Nome).pdf`, com as explicações e as perguntas prováveis. Para trocar quem fala o quê, mude a ordem dos nomes no `config.json` e gere de novo (seção 8.3).

**Pessoa 1, quadrante superior esquerdo (título, objetivo, metodologia).** Apontar para o fluxo 223 → 217 → 30.

> Nosso trabalho compara a Paraíba e o Rio Grande do Norte em três indicadores do IBGE: o IDEB dos anos iniciais da rede pública, a porcentagem da população com renda per capita de até meio salário mínimo e o salário médio dos trabalhadores formais. A pergunta é se os dois estados são diferentes nesses indicadores. Sorteamos 30 municípios de cada estado por amostragem aleatória simples, sem reposição. Seis municípios de cada estado não têm IDEB divulgado e ficaram fora do sorteio, porque precisávamos das três variáveis de cada município. O sorteio foi feito no computador com uma semente fixa, então qualquer pessoa consegue refazer e chegar nos mesmos municípios. As planilhas das duas amostras estão neste QR code.

**Pessoa 2, quadrante superior direito (estatísticas descritivas).** Apontar para as linhas sombreadas e depois para o quadro "O que a tabela mostra".

> A tabela compara, para cada variável, a população inteira com a nossa amostra, que são as linhas sombreadas. As médias da amostra ficaram perto das da população. A maior diferença relativa foi no IDEB da Paraíba, 5,57 contra 5,34, porque a amostra pegou municípios com IDEB alto, como Coxixola, com 8,2, o maior do estado. Comparando os estados: a Paraíba tem IDEB maior, e renda e salário têm centros parecidos, perto de 50% e de 1,8 salário mínimo. O RN varia mais no salário, e a PB varia mais no IDEB. IDEB e salário têm cauda à direita, com poucos municípios de valor bem alto, e a renda tem cauda à esquerda nas populações. Não calculamos a moda porque as três variáveis são contínuas, como diz a observação do enunciado.

**Pessoa 3, quadrante inferior esquerdo (gráficos do salário e IC da proporção).** Apontar para as barras centrais do histograma, para os pontos atípicos e para os triângulos do gráfico do IC.

> Aqui está o salário médio em cada amostra. O histograma mostra quantos municípios caem em cada faixa de 0,2 salário mínimo, e o boxplot resume a distribuição: a caixa vai do primeiro ao terceiro quartil, a linha é a mediana e o losango é a média. A PB é bem concentrada: 24 dos 30 municípios estão de 1,6 a 1,9 salário mínimo. O RN é mais espalhado, de 1,4 a 2,9. Os dois têm cauda à direita, e cada um tem um valor atípico: Carrapateira na PB, com 2,4, e Riachuelo no RN, com 2,9. Embaixo está o intervalo de confiança de 95% para a proporção da população com renda de até meio salário mínimo: de 33,1% a 68,9% na PB e de 31,0% a 66,8% no RN. Os dois acertaram o valor real, que é o triângulo, e quase coincidem. São largos porque a amostra tem só 30 municípios.

**Pessoa 4, quadrante inferior direito (testes de hipóteses e conclusão).** Apontar para a tabela de testes, linha por linha, e depois para a conclusão.

> Para comparar os estados, usamos testes de hipóteses com nível de significância de 5%. Na proporção da renda, o teste z deu p-valor de 0,868, então não há diferença significativa. Para as médias, seguimos a dica do enunciado: primeiro o teste F compara as variâncias, e o resultado decide qual teste t usar. No IDEB, o F não rejeitou variâncias iguais, então usamos o t com variâncias iguais: p-valor de 0,004, rejeitamos a igualdade, e a média da PB é maior. No salário, o F rejeitou variâncias iguais, então usamos o t de Welch: p-valor de 0,126, sem diferença significativa. Concluindo: a educação separa os estados, com a PB à frente no IDEB, enquanto renda e salário são parecidos. O RN é mais heterogêneo no salário. E as amostras representaram bem as populações, porque todos os intervalos de confiança contêm os valores reais.

Dica: cada um deve ler a seção da Questão correspondente (seção 3) e a lista de perguntas abaixo, porque a professora pode perguntar para qualquer integrante.

---

## 6. Perguntas que a professora pode fazer

1. **Por que 6 municípios de cada estado ficaram fora do sorteio?** Eles não têm IDEB divulgado, e cada município da amostra precisava das 3 variáveis. As médias de renda e salário mudam menos de 0,1 com a exclusão.
2. **Por que não calcularam a moda?** As variáveis são quantitativas contínuas, e o enunciado diz que nesse caso a moda não faz sentido. Se ela insistir: os valores que mais se repetem são 4,7 no IDEB da PB (17 municípios na população, 4 na amostra) e 1,8 SM no salário das duas populações (53 municípios na PB, 29 no RN). Essas repetições existem só porque o IBGE arredonda para uma casa decimal; com mais casas, quase todo valor seria único.
3. **Por que a variância da população divide por N e a da amostra por n − 1?** Na população temos todos os municípios, então a variância é o parâmetro. Na amostra, dividir por n compensaria mal o fato de a média amostral estar "ajustada" aos próprios dados, e a variância sairia menor que a real, em média. Dividir por n − 1 corrige esse viés.
4. **Por que o IC da proporção é tão largo (±17,9 p.p.)?** A fórmula p̂(1 − p̂)/n trata cada um dos 30 municípios como um único "sim ou não". Com p̂ perto de 50% e n = 30, a margem fica grande. Na prática, as proporções municipais variam bem menos (desvio padrão de cerca de 3,6 p.p.). Se a renda fosse tratada como uma variável numérica e comparada pelo teste t, o IC da média ficaria com cerca de ±1,3 p.p., e a diferença entre os estados (51,0% contra 48,9%) daria significativa (t = 2,34; p-valor = 0,023). Usamos a fórmula de proporção porque é a que a questão pede; essa diferença de método é a principal ressalva do trabalho.
5. **A "proporção de indivíduos" que vocês estimaram é a proporção do estado?** É a proporção do município médio. Cada município pesa igual, então João Pessoa e Natal contam o mesmo que um município de 2 mil habitantes. A proporção de pessoas do estado inteiro exigiria pesar pelo número de habitantes, que não está nas planilhas.
6. **Por que no IDEB usaram o t com variâncias iguais e no salário o de Welch?** Por causa do teste F, como a dica do enunciado pede. No IDEB, o F não rejeitou variâncias iguais (p-valor 0,303); no salário, rejeitou (p-valor 0,026). Nos dois casos, o outro teste t daria a mesma decisão.
7. **Os dados são normais? Pode usar o teste t?** O Shapiro-Wilk aponta desvios da normal (salário nos dois estados, IDEB no RN). Com 30 municípios por estado, o Teorema Central do Limite faz a média amostral ter distribuição aproximadamente normal, e o teste t continua válido.
8. **O teste F é confiável aqui?** Ele é sensível à falta de normalidade. No salário, o teste de Levene, que não depende disso, deu p-valor 0,097 (não rejeitaria variâncias iguais). Como os dois testes t chegam na mesma conclusão, a decisão sobre as médias não muda.
9. **O que é o p-valor?** É a probabilidade de observar uma diferença tão grande quanto a da amostra, ou maior, se H₀ fosse verdadeira. No IDEB, p-valor = 0,004: se as médias fossem iguais, uma diferença como a nossa apareceria em só 0,4% das amostras, então rejeitamos H₀. Ele não mede a probabilidade de H₀ ser verdadeira.
10. **A diferença no IDEB quer dizer que a escola da PB é melhor?** O teste mostra que a média do IDEB dos anos iniciais da rede pública é maior na PB (0,72 ponto, entre 0,24 e 1,20 com 95% de confiança). Ele não mostra a causa, e o IDEB mede só uma etapa da rede pública.
11. **Por que a média do IDEB na amostra da PB (5,57) ficou acima da população (5,34)?** Variação de amostragem: o sorteio pegou vários municípios de IDEB alto. O IC de 95% da média (5,19 a 5,95) contém o valor real.
12. **No script de exemplo, o IC da média usa z e o desvio padrão da população. Por que vocês usaram t?** Na prática, quem tem só a amostra não conhece o desvio padrão da população, então usa s e a distribuição t. Com o desvio padrão da população (como no exemplo), os intervalos seriam: IDEB PB 5,28 a 5,86; IDEB RN 4,61 a 5,09; salário PB 1,70 a 1,86; salário RN 1,77 a 1,99. Todos também contêm o valor real.
13. **Por que usar z no IC da proporção?** Pela aproximação normal da binomial, que vale quando n·p̂ e n·(1 − p̂) são pelo menos 5. Aqui, 30 × 0,51 ≈ 15.
14. **E se fosse outra amostra?** Os números mudariam um pouco. O IC de 95% acerta o valor real em cerca de 95% das amostras possíveis; aqui os 6 intervalos acertaram.
15. **Por que o Q1 do salário é 1,625 se nenhum município tem 1,625?** O quartil é calculado por interpolação entre dois valores da lista ordenada (método padrão do R e do Excel). No cartaz, aparece arredondado como 1,62 pela regra da ABNT.
16. **Por que Carrapateira e Riachuelo são atípicos?** Pela regra do boxplot: o salário deles passa de Q3 + 1,5·AIQ (2,31 SM na PB e 2,56 SM no RN). Os dados não dizem a causa.

---

## 7. Glossário rápido

- **População / amostra:** todos os municípios do estado / os 30 sorteados.
- **Parâmetro / estimativa:** o valor da população (μ, σ², p) / o valor calculado na amostra (x̄, s², p̂).
- **AAS (amostragem aleatória simples):** todo município tem a mesma chance de ser sorteado.
- **Semente:** número que fixa o sorteio do computador, para ele poder ser repetido.
- **Média / mediana:** soma dividida pela quantidade / valor do meio da lista ordenada.
- **Variância / desvio padrão:** quanto os valores se afastam da média; o desvio padrão é a raiz da variância e fica na mesma unidade dos dados.
- **CV (coeficiente de variação):** desvio padrão dividido pela média; serve para comparar dispersões de variáveis diferentes.
- **Quartis (Q1, Q3) e AIQ:** Q1 deixa 25% dos dados abaixo e Q3 deixa 75%; AIQ = Q3 − Q1 mede a dispersão dos 50% centrais.
- **Assimetria:** cauda à direita (positiva) quando poucos valores são bem maiores que os demais; cauda à esquerda (negativa) quando poucos são bem menores.
- **Histograma:** barras com a quantidade de municípios em cada faixa de valores.
- **Boxplot:** caixa de Q1 a Q3, linha na mediana, bigodes até os valores dentro dos limites, pontos para os atípicos.
- **Valor atípico (outlier):** valor abaixo de Q1 − 1,5·AIQ ou acima de Q3 + 1,5·AIQ.
- **IC de 95% (intervalo de confiança):** faixa calculada pela amostra que contém o valor real em 95% das amostras possíveis.
- **H₀ / H₁:** hipótese nula (não há diferença) / hipótese alternativa (há diferença).
- **α (nível de significância):** o risco aceito de rejeitar H₀ quando ela é verdadeira; aqui, 5%.
- **p-valor:** probabilidade de ver uma diferença tão grande quanto a observada se H₀ fosse verdadeira; p-valor < 0,05 leva a rejeitar H₀.
- **Teste z de duas proporções:** compara duas proporções.
- **Teste F:** compara duas variâncias (razão s²₁/s²₂).
- **Teste t (variância combinada / Welch):** compara duas médias, supondo variâncias iguais / diferentes.
- **gl (graus de liberdade):** parâmetro das distribuições t e F que depende do tamanho das amostras.
- **Shapiro-Wilk:** testa se os dados parecem vir de uma distribuição normal.
- **Levene:** testa a igualdade de variâncias sem depender de normalidade.
- **Teorema Central do Limite (TCL):** com amostras grandes (na prática, n ≥ 30), a média amostral tem distribuição aproximadamente normal, seja qual for a distribuição dos dados.

---

## 8. Como preencher, gerar de novo e imprimir

### 8.1 Subir a planilha e pegar o link

1. Abra o Google Drive com a conta de alguém do grupo.
2. Clique em "Novo" > "Upload de arquivo" e escolha `dados/amostras.xlsx`.
3. Clique com o botão direito no arquivo > "Compartilhar".
4. Em "Acesso geral", troque "Restrito" por "Qualquer pessoa com o link", com o papel "Leitor".
5. Clique em "Copiar link".
6. Teste o link numa janela anônima do navegador: a planilha precisa abrir sem pedir login.

### 8.2 Preencher o `cartaz/config.json`

Abra o arquivo no VS Code ou no Bloco de Notas e troque os valores entre aspas. Mantenha as aspas, as vírgulas e os colchetes. A lista de nomes aceita quantos integrantes forem.

```json
{
  "grupo": "Grupo 3",
  "integrantes": ["Augusto Blois", "Nome Sobrenome", "Nome Sobrenome", "Nome Sobrenome"],
  "link_planilhas": "https://drive.google.com/file/d/..../view?usp=sharing"
}
```

### 8.3 Gerar o cartaz de novo (PowerShell)

```powershell
Set-Location "C:\Users\augus\workspace\faculdade\p3\metodos-estatisticos\projeto-un2"
python cartaz\montar_cartaz.py
python falas\gerar_falas.py
```

O primeiro comando gera o cartaz; o segundo gera os PDFs de falas a partir do cartaz pronto, por isso vem depois. O esperado é a linha "Cartaz gerado em ..." sem nenhuma linha "ATENÇÃO", seguida de uma linha por integrante. O QR code é gerado sozinho a partir do link. Se aparecer "conteúdo passou da borda", algum nome ficou comprido demais: use só nome e sobrenome. Não é preciso rodar o `analise\analise.py` de novo; ele só serve se os dados ou a semente mudarem (e, com a mesma semente, ele gera exatamente a mesma amostra).

Depois de gerar, abra o `cartaz/cartaz_A2.pdf`, confira os nomes e aponte a câmera do celular para o QR code: ele deve abrir a planilha.

### 8.4 Imprimir

Em qualquer opção: imprimir colorido e em "Tamanho real" (100%), sem "Ajustar à página". Cada folha tem margem de 8 mm, então a borda que a impressora não imprime não corta nada.

- **4 folhas A4, em casa (plano mais seguro):** imprima o `cartaz_4xA4.pdf`. Folha 1 = canto superior esquerdo, 2 = superior direito, 3 = inferior esquerdo, 4 = inferior direito. Cole 2 × 2 numa cartolina (50 × 66 cm), deixando as folhas encostadas; o espaço entre os quadros já faz parte do desenho. O conjunto ocupa 42 × 59,4 cm e sobra uma moldura de 3 a 4 cm.
- **2 folhas A3, em copiadora:** imprima o `cartaz_2xA3.pdf` (folhas deitadas). Folha 1 = metade de cima, 2 = metade de baixo. Cole uma sobre a outra na cartolina.
- **1 folha A2, em gráfica:** leve o `cartaz_A2.pdf`. Se a gráfica oferecer A1, pode ampliar sem perder qualidade. Ela pode imprimir direto em papel mais grosso, e aí a cartolina vira só o suporte.

O enunciado aceita "partes impressas e coladas" em cartolina ou semelhante, então as três opções valem. Como a apresentação é na segunda, a impressão em casa evita depender do horário de gráfica.
