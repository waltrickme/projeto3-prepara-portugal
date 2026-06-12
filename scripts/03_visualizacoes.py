"""
Gráfico 1: Top 10 cargos mais frequentes (barras horizontais)
Gráfico 2: Top 10 empresas mais recorrentes (barras horizontais)
Gráfico 3: Distribuição geográfica Brasil / México / Outros (barras)
Gráfico 4: Distribuição por área profissional (pizza)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

PROCESSED_PATH = "data/processed/leads_harmonizados.xlsx"
GRAFICOS_DIR = "outputs/graficos"

sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.family": "sans-serif", "figure.dpi": 150})

# Paleta idêntica ao Looker Studio (tema Google)
LOOKER_BLUE  = "#4285F4"
LOOKER_GREEN = "#34A853"
LOOKER_PIE   = ["#4285F4", "#EA8600", "#9334E6", "#34A853", "#13B5C8", "#FBBC04"]

AREA_MAP = {
    "Legal": ["attorney", "lawyer", "counsel", "legal", "paralegal", "law"],
    "Compliance": ["compliance", "regulatory", "risk", "aml", "kyc", "pld"],
    "Finance": ["finance", "financeiro", "treasury", "controller", "cfo", "financ"],
    "Technology": ["tech", "engineer", "developer", "software", "data", "it ", "product", "devops"],
    "Comercial": ["sales", "comercial", "business", "account", "vendas", "revenue"],
}


def classify_area(cargo: str) -> str:
    if not isinstance(cargo, str) or cargo.lower() == "desconhecido":
        return "Outros"
    lower = cargo.lower()
    for area, keywords in AREA_MAP.items():
        if any(kw in lower for kw in keywords):
            return area
    return "Outros"


def grafico1(df):
    top10 = df[df["cargo"] != "Desconhecido"]["cargo"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top10.index[::-1], top10.values[::-1], color=LOOKER_BLUE)
    ax.set_xlabel("Número de Leads")
    ax.set_title("Top 10 Cargos Mais Frequentes", fontsize=14, fontweight="bold", pad=15)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    path = f"{GRAFICOS_DIR}/grafico1_cargos.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


def grafico2(df):
    top10 = (
        df[df["empresa_harmonizada"] != "Desconhecido"]["empresa_harmonizada"]
        .value_counts()
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top10.index[::-1], top10.values[::-1], color=LOOKER_GREEN)
    ax.set_xlabel("Número de Leads")
    ax.set_title("Top 10 Empresas Mais Recorrentes", fontsize=14, fontweight="bold", pad=15)
    for bar, val in zip(bars, top10.values[::-1]):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    path = f"{GRAFICOS_DIR}/grafico2_empresas.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


def grafico3(df):
    """Gráfico 3 obrigatório: Brasil / México / Outros (conforme enunciado)."""
    por_pais = df["pais_padronizado"].value_counts()  # ordem decrescente: Outros, Brasil, México
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(por_pais.index, por_pais.values, color=LOOKER_BLUE, width=0.5)
    ax.set_ylabel("Número de Leads")
    ax.set_title("Distribuição Geográfica dos Leads", fontsize=14, fontweight="bold", pad=15)
    for bar, val in zip(bars, por_pais.values):
        pct = val / len(df) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                f"{val}\n({pct:.1f}%)", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, por_pais.max() * 1.2)
    plt.tight_layout()
    path = f"{GRAFICOS_DIR}/grafico3_paises.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


def grafico4(df):
    df = df.copy()
    df["area"] = df["cargo"].apply(classify_area)
    por_area = df["area"].value_counts()
    colors = LOOKER_PIE[:len(por_area)]
    fig, ax = plt.subplots(figsize=(7, 7))
    def autopct_large_only(pct):
        return f"{pct:.1f}%" if pct >= 4.0 else ""

    total = por_area.values.sum()
    wedges, texts, autotexts = ax.pie(
        por_area.values,
        labels=None,
        autopct=autopct_large_only,
        colors=colors,
        startangle=90,
        counterclock=False,
        pctdistance=0.75,
    )
    for text in autotexts:
        text.set_fontsize(10)
    # Legenda com percentagem em todas as categorias (incluindo as pequenas)
    legend_labels = [
        f"{area}  {val/total*100:.1f}%"
        for area, val in zip(por_area.index, por_area.values)
    ]
    ax.legend(
        wedges,
        legend_labels,
        title="Área",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10,
    )
    ax.set_title("Distribuição por Área Profissional", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    path = f"{GRAFICOS_DIR}/grafico4_areas.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {path}")


def main():
    print("A carregar base harmonizada...")
    df = pd.read_excel(PROCESSED_PATH)
    print(f"  {len(df)} registos\n")

    print("A gerar gráficos...")
    grafico1(df)
    grafico2(df)
    grafico3(df)
    grafico4(df)

    print("\nTodos os gráficos gerados com sucesso.")


if __name__ == "__main__":
    main()
