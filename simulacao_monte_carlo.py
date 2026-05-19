from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from simulacao_faturamento import DESVIO_PADRAO, MEDIA, MESES

N_SIMULACOES = 10_000
PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_CSV = PASTA_PROJETO / "monte_carlo_simulacoes.csv"
ARQUIVO_GRAFICO = PASTA_PROJETO / "monte_carlo_graficos.png"


def executar_monte_carlo(n_simulacoes: int, meses: int, media: float, desvio: float) -> np.ndarray:
    valores = np.random.normal(loc=media, scale=desvio, size=(n_simulacoes, meses))
    return np.maximum(valores, 0)


def montar_dataframe(simulacoes: np.ndarray) -> pd.DataFrame:
    colunas_meses = [f"Mês {i:02d}" for i in range(1, MESES + 1)]
    df_largo = pd.DataFrame(simulacoes, columns=colunas_meses)
    df_largo.insert(0, "simulação", range(1, len(df_largo) + 1))

    df = df_largo.melt(
        id_vars="simulação",
        var_name="mês",
        value_name="faturamento mensal",
    )
    df["faturamento mensal"] = df["faturamento mensal"].round(2)
    return df


def calcular_estatisticas(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("mês", sort=False)["faturamento mensal"]
        .agg(média="mean", mínimo="min", máximo="max")
        .round(2)
    )


def gerar_grafico(simulacoes: np.ndarray, stats: pd.DataFrame, colunas_meses: list[str]) -> None:
    meses_x = np.arange(1, MESES + 1)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for trajetoria in simulacoes:
        axes[0].plot(meses_x, trajetoria, color="gray", alpha=0.08, linewidth=0.8)

    axes[0].plot(meses_x, stats["média"].values, color="blue", linewidth=2.5, label="Média")
    axes[0].plot(meses_x, stats["mínimo"].values, color="red", linewidth=2, linestyle="--", label="Mínimo")
    axes[0].plot(meses_x, stats["máximo"].values, color="green", linewidth=2, linestyle="--", label="Máximo")
    axes[0].axhline(MEDIA, color="orange", linestyle=":", label=f"Média alvo (R$ {MEDIA:,.0f})")
    axes[0].set_title(f"Monte Carlo — {N_SIMULACOES} simulações")
    axes[0].set_xlabel("Mês")
    axes[0].set_ylabel("Faturamento mensal (R$)")
    axes[0].set_xticks(meses_x)
    axes[0].set_xticklabels(colunas_meses, rotation=45)
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    totais_anuais = simulacoes.sum(axis=1)
    axes[1].hist(totais_anuais, bins=40, color="steelblue", edgecolor="black", alpha=0.85)
    axes[1].axvline(totais_anuais.mean(), color="blue", linewidth=2, label=f"Média: R$ {totais_anuais.mean():,.0f}")
    axes[1].axvline(totais_anuais.min(), color="red", linewidth=2, linestyle="--", label=f"Mínimo: R$ {totais_anuais.min():,.0f}")
    axes[1].axvline(totais_anuais.max(), color="green", linewidth=2, linestyle="--", label=f"Máximo: R$ {totais_anuais.max():,.0f}")
    axes[1].set_title("Distribuição do faturamento anual")
    axes[1].set_xlabel("Faturamento anual (R$)")
    axes[1].set_ylabel("Frequência")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(ARQUIVO_GRAFICO, dpi=150)
    plt.close()


def main() -> None:
    np.random.seed(42)
    colunas_meses = [f"Mês {i:02d}" for i in range(1, MESES + 1)]

    simulacoes = executar_monte_carlo(N_SIMULACOES, MESES, MEDIA, DESVIO_PADRAO)
    df = montar_dataframe(simulacoes)
    stats_mensais = calcular_estatisticas(df)

    totais_anuais = df.groupby("simulação")["faturamento mensal"].sum()

    print("=" * 60)
    print("SIMULAÇÃO MONTE CARLO — LOJA DE ROUPAS")
    print("=" * 60)
    print(f"Simulações:      {N_SIMULACOES}")
    print(f"Meses por sim.:  {MESES}")
    print(f"Distribuição:    Normal(μ={MEDIA:,.0f}, σ={DESVIO_PADRAO:,.0f})")
    print(f"Registros:       {len(df):,} linhas no DataFrame")
    print("-" * 60)
    print("\nEstatísticas mensais (entre todas as simulações):")
    print(stats_mensais.to_string())
    print("-" * 60)
    print("\nFaturamento anual por simulação:")
    print(f"  Média:   R$ {totais_anuais.mean():,.2f}")
    print(f"  Mínimo:  R$ {totais_anuais.min():,.2f}")
    print(f"  Máximo:  R$ {totais_anuais.max():,.2f}")
    print("=" * 60)

    df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig", float_format="%.2f")
    print(f"\nCSV salvo em:\n  {ARQUIVO_CSV}")

    gerar_grafico(simulacoes, stats_mensais, colunas_meses)
    print(f"Gráfico salvo em:\n  {ARQUIVO_GRAFICO}")


if __name__ == "__main__":
    main()
