from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from simulacao_faturamento import DESVIO_PADRAO, MEDIA, MESES, PASTA_PROJETO
from simulacao_monte_carlo import N_SIMULACOES, executar_monte_carlo

ARQUIVO_REAL = PASTA_PROJETO / "faturamento_real.csv"
ARQUIVO_MONTE_CARLO = PASTA_PROJETO / "monte_carlo_simulacoes.csv"
ARQUIVO_COMPARACAO = PASTA_PROJETO / "comparacao_final.csv"
ARQUIVO_RELATORIO = PASTA_PROJETO / "relatorio_final.md"
ARQUIVO_GRAFICO = PASTA_PROJETO / "comparacao_graficos.png"


def carregar_faturamento_real() -> pd.DataFrame:
    if not ARQUIVO_REAL.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_REAL}\n"
            "Execute antes: python simulacao_faturamento.py"
        )
    return pd.read_csv(ARQUIVO_REAL, encoding="utf-8-sig")


def carregar_media_simulada() -> pd.Series:
    if ARQUIVO_MONTE_CARLO.exists():
        df_mc = pd.read_csv(ARQUIVO_MONTE_CARLO, encoding="utf-8-sig")
        return (
            df_mc.groupby("mês", sort=False)["faturamento mensal"]
            .mean()
            .round(2)
        )

    np.random.seed(42)
    simulacoes = executar_monte_carlo(N_SIMULACOES, MESES, MEDIA, DESVIO_PADRAO)
    colunas = [f"Mês {i:02d}" for i in range(1, MESES + 1)]
    return pd.Series(simulacoes.mean(axis=0), index=colunas).round(2)


def montar_tabela_comparativa(df_real: pd.DataFrame, media_simulada: pd.Series) -> pd.DataFrame:
    comparacao = df_real[["mês", "faturamento mensal"]].copy()
    comparacao = comparacao.rename(columns={"faturamento mensal": "faturamento real"})

    comparacao["média simulada"] = comparacao["mês"].map(media_simulada)
    comparacao["diferença"] = (comparacao["faturamento real"] - comparacao["média simulada"]).round(2)
    comparacao["diferença (%)"] = (
        (comparacao["diferença"] / comparacao["média simulada"]) * 100
    ).round(2)

    return comparacao


def adicionar_linha_total(comparacao: pd.DataFrame) -> pd.DataFrame:
    total = pd.DataFrame([{
        "mês": "Total anual",
        "faturamento real": comparacao["faturamento real"].sum(),
        "média simulada": comparacao["média simulada"].sum(),
        "diferença": comparacao["diferença"].sum(),
        "diferença (%)": round(
            (comparacao["diferença"].sum() / comparacao["média simulada"].sum()) * 100, 2
        ),
    }])
    return pd.concat([comparacao, total], ignore_index=True)


def gerar_graficos(comparacao: pd.DataFrame) -> None:
    meses = comparacao["mês"].tolist()
    x = np.arange(len(meses))
    largura = 0.35

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].bar(x - largura / 2, comparacao["faturamento real"], largura, label="Real", color="steelblue")
    axes[0].bar(x + largura / 2, comparacao["média simulada"], largura, label="Média simulada", color="coral")
    axes[0].set_title("Faturamento mensal: real vs média simulada")
    axes[0].set_xlabel("Mês")
    axes[0].set_ylabel("Faturamento (R$)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(meses, rotation=45)
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    axes[1].plot(meses, comparacao["faturamento real"], marker="o", linewidth=2, label="Real", color="steelblue")
    axes[1].plot(meses, comparacao["média simulada"], marker="s", linewidth=2, label="Média simulada", color="coral")
    axes[1].axhline(MEDIA, color="red", linestyle="--", alpha=0.7, label=f"Média alvo (R$ {MEDIA:,.0f})")
    axes[1].set_title("Evolução comparativa")
    axes[1].set_xlabel("Mês")
    axes[1].set_ylabel("Faturamento (R$)")
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(ARQUIVO_GRAFICO, dpi=150)
    plt.close()


def _dataframe_para_markdown(df: pd.DataFrame) -> str:
    cabecalho = "| " + " | ".join(df.columns) + " |"
    separador = "| " + " | ".join(["---"] * len(df.columns)) + " |"
    linhas = []
    for _, row in df.iterrows():
        valores = []
        for col in df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "mês":
                valores.append(f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            else:
                valores.append(str(val))
        linhas.append("| " + " | ".join(valores) + " |")
    return "\n".join([cabecalho, separador, *linhas])


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_relatorio(comparacao: pd.DataFrame, comparacao_com_total: pd.DataFrame) -> None:
    meses_acima = comparacao[comparacao["diferença"] > 0]
    meses_abaixo = comparacao[comparacao["diferença"] < 0]
    erro_medio_abs = comparacao["diferença"].abs().mean()
    total_real = comparacao["faturamento real"].sum()
    total_simulado = comparacao["média simulada"].sum()
    total_diff = comparacao["diferença"].sum()

    tabela_md = _dataframe_para_markdown(comparacao_com_total)

    conteudo = f"""# Relatório Final — Comparação Monte Carlo vs Faturamento Real

## Descrição do projeto

Este projeto modela e projeta o faturamento mensal de uma **loja de roupas** ao longo de **12 meses** de operação. O trabalho combina três etapas:

1. **Faturamento real simulado** — uma trajetória mensal gerada por distribuição normal, representando o cenário observado da loja.
2. **Simulação de Monte Carlo** — milhares de cenários possíveis para quantificar a incerteza do faturamento.
3. **Comparação final** — consolidação das simulações mês a mês e confronto com o faturamento real.

O objetivo é avaliar se o faturamento real observado está alinhado com o comportamento esperado pelo modelo estocástico.

## Metodologia utilizada

- Geração do **faturamento real** com distribuição normal truncada em zero (valores negativos são descartados).
- Execução de **{N_SIMULACOES:,} simulações independentes**, cada uma com 12 meses de faturamento.
- **Consolidação** das simulações pela média aritmética mensal entre todos os cenários.
- **Comparação** entre a média simulada e o faturamento real, com cálculo da diferença absoluta e percentual.
- Visualização gráfica em barras e linhas para análise visual das divergências.

## Parâmetros da distribuição normal

| Parâmetro | Valor |
|-----------|-------|
| Média (μ) | {formatar_moeda(MEDIA)} |
| Desvio padrão (σ) | {formatar_moeda(DESVIO_PADRAO)} |
| Meses analisados | {MESES} |
| Truncamento inferior | R$ 0,00 (sem faturamento negativo) |

## Quantidade de simulações

Foram executadas **{N_SIMULACOES:,} simulações de Monte Carlo**, totalizando **{N_SIMULACOES * MESES:,}** registros mensais simulados ({N_SIMULACOES:,} cenários × {MESES} meses).

## Análise dos resultados

### Resumo consolidado

| Indicador | Valor |
|-----------|-------|
| Faturamento real total (12 meses) | {formatar_moeda(total_real)} |
| Média simulada total (12 meses) | {formatar_moeda(total_simulado)} |
| Diferença total (real − simulado) | {formatar_moeda(total_diff)} |
| Erro médio absoluto mensal | {formatar_moeda(erro_medio_abs)} |
| Meses com real acima da média simulada | {len(meses_acima)} |
| Meses com real abaixo da média simulada | {len(meses_abaixo)} |

### Tabela comparativa

{tabela_md}

> A linha **Total anual** soma os valores mensais. A diferença percentual do total é calculada sobre a média simulada acumulada.

## Comparação entre faturamento real e simulado

A média das {N_SIMULACOES:,} simulações representa o **faturamento esperado** pelo modelo em cada mês. O faturamento real difere dessa expectativa em alguns períodos:

"""

    for _, linha in comparacao.iterrows():
        sinal = "acima" if linha["diferença"] > 0 else "abaixo" if linha["diferença"] < 0 else "igual à"
        conteudo += (
            f"- **{linha['mês']}**: real {formatar_moeda(linha['faturamento real'])} vs "
            f"média simulada {formatar_moeda(linha['média simulada'])} "
            f"({sinal} da média em {formatar_moeda(abs(linha['diferença']))}, "
            f"{linha['diferença (%)']:+.2f}%).\n"
        )

    if total_diff > 0:
        tendencia = "superior"
    elif total_diff < 0:
        tendencia = "inferior"
    else:
        tendencia = "equivalente"

    conteudo += f"""
O faturamento real anual foi **{tendencia}** à média consolidada das simulações em {formatar_moeda(abs(total_diff))} ({abs(total_diff / total_simulado * 100):.2f}% em relação à média simulada anual).

O gráfico comparativo está disponível em: `comparacao_graficos.png`.

## Conclusão final

O modelo de Monte Carlo com distribuição Normal(μ={MEDIA:,.0f}, σ={DESVIO_PADRAO:,.0f}) produz uma faixa de cenários compatível com o faturamento real da loja. A consolidação por média mensal permite verificar se o resultado observado é **estatisticamente plausível** dentro do modelo.

"""

    if abs(total_diff / total_simulado * 100) < 5:
        conteudo += (
            "O faturamento real anual apresentou divergência **moderada** em relação à média simulada, "
            "indicando boa aderência do modelo ao cenário gerado. Variações mensais pontuais são esperadas "
            "em processos estocásticos, mesmo quando a média de longo prazo converge para μ.\n"
        )
    else:
        conteudo += (
            "O faturamento real apresentou divergência **mais expressiva** em relação à média simulada em alguns meses, "
            "o que reforça a importância de analisar cenários individuais além da média. "
            "Recomenda-se revisar sazonalidade, promoções ou mudanças operacionais não capturadas pelo modelo base.\n"
        )

    conteudo += (
        "\n---\n\n"
        "*Relatório gerado automaticamente por `comparacao_final.py`.*\n"
    )

    ARQUIVO_RELATORIO.write_text(conteudo, encoding="utf-8")


def main() -> None:
    df_real = carregar_faturamento_real()
    media_simulada = carregar_media_simulada()

    comparacao = montar_tabela_comparativa(df_real, media_simulada)
    comparacao_com_total = adicionar_linha_total(comparacao)

    print("=" * 70)
    print("COMPARAÇÃO FINAL — FATURAMENTO REAL vs MONTE CARLO")
    print("=" * 70)
    print(comparacao_com_total.to_string(index=False))
    print("=" * 70)

    comparacao_com_total.to_csv(
        ARQUIVO_COMPARACAO, index=False, encoding="utf-8-sig", float_format="%.2f"
    )
    gerar_graficos(comparacao)
    gerar_relatorio(comparacao, comparacao_com_total)

    print(f"\nCSV salvo em:\n  {ARQUIVO_COMPARACAO}")
    print(f"Gráfico salvo em:\n  {ARQUIVO_GRAFICO}")
    print(f"Relatório salvo em:\n  {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
