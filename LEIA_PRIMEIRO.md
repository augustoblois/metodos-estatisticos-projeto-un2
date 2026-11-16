# Projeto corrigido: o que fazer agora

1. Leia `falas/fala_simples_Luy.md`: é sua fala de cerca de 1 minuto e meio, em cinco blocos, com indicações de onde apontar.
2. Abra `falas/falas (Luy Koji).pdf`: contém a fala, conceitos e perguntas prováveis, além da imagem da sua parte do cartaz.
3. Compartilhe as falas novas com Augusto, Pedro e Luiz. Usem todos a mesma versão do cartaz.
4. Alinhem com a professora a adaptação da questão 3 para média dos percentuais municipais e a restrição às bases elegíveis do sorteio original.
5. Confiram que o link do QR code abre sem login e contém as planilhas certas. Esta revisão não alterou o Google Drive.
6. Para imprimir em casa, use `cartaz/cartaz_4xA4.pdf`, colorido e em 100%, quatro folhas em 2×2. Há também versões em uma A2 e duas A3.

## Mudanças importantes

- Sorteio preservado: mesmos 30 municípios por estado, mesmos dados, ordem e semente.
- Renda: média dos percentuais municipais nas bases elegíveis de 217 (PB) e 161 (RN), não proporção estadual de pessoas.
- Correção de população finita em todos os ICs e comparações principais das médias.
- IC de 95% da renda: PB 49,77% a 52,26%; RN 47,68% a 50,05%.
- Comparações aproximadas, com CPF: renda p≈0,013; IDEB p≈0,002; salário p≈0,094.
- Não há afirmações causais, garantia de normalidade por n=30 ou prova de representatividade por cobertura dos ICs.
- As planilhas originais e a planilha das amostras foram mantidas. Resultados, gráficos, relatório, cartaz e quatro falas foram atualizados.

Os scripts e `requirements.txt` estão incluídos para reprodução. Para usar os PDFs e estudar sua fala, não é necessário instalar Python nem executar comandos. Nada foi publicado no GitHub.

## Limitações que permanecem

A adaptação da questão 3 e as exclusões do sorteio precisam ser alinhadas com a docente. Não é possível transformar a média municipal em proporção estadual sem denominadores compatíveis. Os anos dos indicadores não constam nas planilhas. A calibração t usada nos testes é aproximada e não garante cobertura exata para qualquer população finita.

O relatório apresenta fórmulas, hipóteses, diagnósticos, sensibilidade sem CPF e referências. `saida/verificacao.json` registra a conferência computacional; os PDFs também foram renderizados para inspeção visual nesta revisão.
