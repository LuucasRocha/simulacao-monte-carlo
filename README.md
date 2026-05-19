# Comparação Monte Carlo vs Faturamento Real

## Descrição do projeto

Este projeto modela e projeta o faturamento mensal de uma **loja de roupas** ao longo de **12 meses** de operação. O trabalho combina três etapas:

1. **Faturamento real simulado** — uma trajetória mensal gerada por distribuição normal, representando o cenário observado da loja.
2. **Simulação de Monte Carlo** — milhares de cenários possíveis para quantificar a incerteza do faturamento.
3. **Comparação final** — consolidação das simulações mês a mês e confronto com o faturamento real.

O objetivo é avaliar se o faturamento real observado está alinhado com o comportamento esperado pelo modelo estocástico.

## Metodologia utilizada

- Geração do **faturamento real** com distribuição normal truncada em zero (valores negativos são descartados).
- Execução de **10,000 simulações independentes**, cada uma com 12 meses de faturamento.
- **Consolidação** das simulações pela média aritmética mensal entre todos os cenários.
- **Comparação** entre a média simulada e o faturamento real, com cálculo da diferença absoluta e percentual.
- Visualização gráfica em barras e linhas para análise visual das divergências.

## Parâmetros da distribuição normal

| Parâmetro | Valor |
|-----------|-------|
| Média (μ) | R$ 80.000,00 |
| Desvio padrão (σ) | R$ 10.000,00 |
| Meses analisados | 12 |
| Truncamento inferior | R$ 0,00 (sem faturamento negativo) |

## Quantidade de simulações

Foram executadas **10,000 simulações de Monte Carlo**, totalizando **120,000** registros mensais simulados (10,000 cenários × 12 meses).

## Análise dos resultados

### Resumo consolidado

| Indicador | Valor |
|-----------|-------|
| Faturamento real total (12 meses) | R$ 960.084,97 |
| Média simulada total (12 meses) | R$ 960.258,95 |
| Diferença total (real − simulado) | R$ -173,98 |
| Erro médio absoluto mensal | R$ 4.275,21 |
| Meses com real acima da média simulada | 5 |
| Meses com real abaixo da média simulada | 7 |

### Tabela comparativa

| mês | faturamento real | média simulada | diferença | diferença (%) |
| --- | --- | --- | --- | --- |
| Mês 01 | 78.559,10 | 80.058,99 | -1.499,89 | -1,87 |
| Mês 02 | 78.270,96 | 79.932,00 | -1.661,04 | -2,08 |
| Mês 03 | 78.886,84 | 80.073,43 | -1.186,59 | -1,48 |
| Mês 04 | 87.019,84 | 79.882,05 | 7.137,79 | 8,94 |
| Mês 05 | 78.724,12 | 80.050,04 | -1.325,92 | -1,66 |
| Mês 06 | 65.026,47 | 80.053,41 | -15.026,94 | -18,77 |
| Mês 07 | 83.323,18 | 80.045,09 | 3.278,09 | 4,10 |
| Mês 08 | 77.326,63 | 80.094,66 | -2.768,03 | -3,46 |
| Mês 09 | 77.830,41 | 80.100,23 | -2.269,82 | -2,83 |
| Mês 10 | 81.158,85 | 79.866,68 | 1.292,17 | 1,62 |
| Mês 11 | 82.322,98 | 80.080,22 | 2.242,76 | 2,80 |
| Mês 12 | 91.635,59 | 80.022,15 | 11.613,44 | 14,51 |
| Total anual | 960.084,97 | 960.258,95 | -173,98 | -0,02 |

> A linha **Total anual** soma os valores mensais. A diferença percentual do total é calculada sobre a média simulada acumulada.

## Comparação entre faturamento real e simulado

A média das 10,000 simulações representa o **faturamento esperado** pelo modelo em cada mês. O faturamento real difere dessa expectativa em alguns períodos:

- **Mês 01**: real R$ 78.559,10 vs média simulada R$ 80.058,99 (abaixo da média em R$ 1.499,89, -1.87%).
- **Mês 02**: real R$ 78.270,96 vs média simulada R$ 79.932,00 (abaixo da média em R$ 1.661,04, -2.08%).
- **Mês 03**: real R$ 78.886,84 vs média simulada R$ 80.073,43 (abaixo da média em R$ 1.186,59, -1.48%).
- **Mês 04**: real R$ 87.019,84 vs média simulada R$ 79.882,05 (acima da média em R$ 7.137,79, +8.94%).
- **Mês 05**: real R$ 78.724,12 vs média simulada R$ 80.050,04 (abaixo da média em R$ 1.325,92, -1.66%).
- **Mês 06**: real R$ 65.026,47 vs média simulada R$ 80.053,41 (abaixo da média em R$ 15.026,94, -18.77%).
- **Mês 07**: real R$ 83.323,18 vs média simulada R$ 80.045,09 (acima da média em R$ 3.278,09, +4.10%).
- **Mês 08**: real R$ 77.326,63 vs média simulada R$ 80.094,66 (abaixo da média em R$ 2.768,03, -3.46%).
- **Mês 09**: real R$ 77.830,41 vs média simulada R$ 80.100,23 (abaixo da média em R$ 2.269,82, -2.83%).
- **Mês 10**: real R$ 81.158,85 vs média simulada R$ 79.866,68 (acima da média em R$ 1.292,17, +1.62%).
- **Mês 11**: real R$ 82.322,98 vs média simulada R$ 80.080,22 (acima da média em R$ 2.242,76, +2.80%).
- **Mês 12**: real R$ 91.635,59 vs média simulada R$ 80.022,15 (acima da média em R$ 11.613,44, +14.51%).

O faturamento real anual foi **inferior** à média consolidada das simulações em R$ 173,98 (0.02% em relação à média simulada anual).

O gráfico comparativo está disponível em: `comparacao_graficos.png`.

## Conclusão final

O modelo de Monte Carlo com distribuição Normal(μ=80,000, σ=10,000) produz uma faixa de cenários compatível com o faturamento real da loja. A consolidação por média mensal permite verificar se o resultado observado é **estatisticamente plausível** dentro do modelo.

O faturamento real anual apresentou divergência **moderada** em relação à média simulada, indicando boa aderência do modelo ao cenário gerado. Variações mensais pontuais são esperadas em processos estocásticos, mesmo quando a média de longo prazo converge para μ.

---

*Relatório gerado automaticamente por `comparacao_final.py`.*
