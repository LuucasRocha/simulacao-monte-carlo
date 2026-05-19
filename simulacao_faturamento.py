from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

MESES = 12
MEDIA = 80_000
DESVIO_PADRAO = 10_000
PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_CSV = PASTA_PROJETO / "faturamento_real.csv"
ARQUIVO_GRAFICO = PASTA_PROJETO / "faturamento_graficos.png"


def simular_faturamento(meses: int, media: float, desvio: float) -> np.ndarray:
    valores = np.random.normal(loc=media, scale=desvio, size=meses)
    return np.maximum(valores, 0)


def main() -> None:
    np.random.seed(42)

    meses = [f"Mês {i:02d}" for i in range(1, MESES + 1)]
    faturamento = simular_faturamento(MESES, MEDIA, DESVIO_PADRAO)

    df = pd.DataFrame({
        "mês": meses,
        "faturamento mensal": np.round(faturamento, 2),
    })
    df["faturamento acumulado"] = df["faturamento mensal"].cumsum().round(2)

    print("=" * 50)
    print("FATURAMENTO MENSAL - LOJA DE ROUPAS")
    print("=" * 50)
    print(df.to_string(index=False))
    print("-" * 50)
    print(f"Total anual:     R$ {df['faturamento mensal'].sum():,.2f}")
    print(f"Média mensal:    R$ {df['faturamento mensal'].mean():,.2f}")
    print(f"Desvio padrão:   R$ {df['faturamento mensal'].std():,.2f}")
    print(f"Mínimo mensal:   R$ {df['faturamento mensal'].min():,.2f}")
    print(f"Máximo mensal:   R$ {df['faturamento mensal'].max():,.2f}")
    print("=" * 50)

    df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig", float_format="%.2f")
    print(f"\nDados salvos em:\n  {ARQUIVO_CSV}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].bar(meses, df["faturamento mensal"], color="steelblue", edgecolor="black")
    axes[0].axhline(MEDIA, color="red", linestyle="--", label=f"Média alvo (R$ {MEDIA:,.0f})")
    axes[0].set_title("Faturamento Mensal")
    axes[0].set_xlabel("Mês")
    axes[0].set_ylabel("Faturamento (R$)")
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    axes[1].plot(meses, df["faturamento mensal"], marker="o", color="darkgreen", linewidth=2)
    axes[1].axhline(MEDIA, color="red", linestyle="--", label=f"Média alvo (R$ {MEDIA:,.0f})")
    axes[1].set_title("Evolução do Faturamento")
    axes[1].set_xlabel("Mês")
    axes[1].set_ylabel("Faturamento (R$)")
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(ARQUIVO_GRAFICO, dpi=150)
    print(f"Gráfico salvo em:\n  {ARQUIVO_GRAFICO}")


if __name__ == "__main__":
    main()
