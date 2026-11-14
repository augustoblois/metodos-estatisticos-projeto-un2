
#planilha de dados
dados <- read_excel("C:/Users/renil/Meu Drive/Material UFPB/2023.2/Turma 2/Projeto UN3/Bancodedados.xlsx")

summary(dados$IDHM)   # estatísticas descritivas
summary(dados$IDEBin) # estatísticas descritivas
summary(dados$IDEBfi) # estatísticas descritivas

mu1  =  mean(dados$IDEBin) # calcula a média
var1 = var(dados$IDEBin) # calcula a variância

hist(dados$IDEBin, freq = F) #faz o histograma
boxplot(dados$IDEBin)   #faz o boxplot

#ajuste da Normal
shapiro.test(dados$IDEBin) #teste de normalidade

#Comando para construir o histograma da variável Enade
hist(dados$IDEBin,freq=FALSE,xlim=c(3,5.7),ylim=c(0,1.0),main=" "
     ,xlab = "IDEB Anos Iniciais", ylab= "Densidade de Frequência")

########### Ajuste da dist. normal com a  media e variancia conhecidas ##############
a= seq(0,5.6,0.01)
lines(a,dnorm(a,mu1, sqrt(var1)),col=4,lwd=3,lty=1)


#intervalo de confiança
#set.seed(1234)
amostra = sample(dados$IDEBin, 10) # seleciona uma amostra aleatória
media_amostra= mean(amostra) # media amostral

alpha = 0.05 # nível de significancia
zc <- qnorm(p = 1-alpha/2, mean = 0, sd = 1) # cálculo do quantil
sigma = sqrt(var1) # desvio padrão populacional
n = 10 # tamanho da amostra
erro <- zc*sigma/sqrt(n) # erro-padrão
lim_inf = media_amostra - erro
lim_sup = media_amostra + erro
mu1>=lim_inf & mu1<=lim_sup

#Regressão
x<- log(dados$POPULACAO)
y<- dados$NEstDeEF
plot(x,y) #gráfico de dispersão
cor(x,y) # calcula a correlação entre as variáveis

regressao<-lm(y~x,data=dados) # modelo de regressão y = ax + b
regressao

z = plot(x,y)
grid(z) #aplicando grid ao gráfico
abline(regressao) # traça a reta de regressão

