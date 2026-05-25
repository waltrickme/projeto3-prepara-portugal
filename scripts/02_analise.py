"""
Pergunta 1: Quantos e-mails inválidos?
Pergunta 2: Quais os 5 cargos mais frequentes?
Pergunta 3: Quantas empresas únicas existem?
Pergunta 4: Qual empresa aparece mais vezes?
Pergunta 5: Quantos leads existem em cada país?
"""

import pandas as pd

PROCESSED_PATH = "data/processed/leads_harmonizados.xlsx"
OUT_PATH = "outputs/analise_resultados.txt"


def main():
    print("A carregar base harmonizada...")
    df = pd.read_excel(PROCESSED_PATH)
    print(f"  {len(df)} registos carregados\n")

    resultados = []

    # Pergunta 1: e-mails inválidos
    invalidos = (~df["email_valido"]).sum()
    duplicados = df["email_duplicado"].sum()
    p1 = (
        f"1. E-mails inválidos (nulos ou formato incorreto): {invalidos} de {len(df)} ({invalidos/len(df)*100:.1f}%)\n"
        f"   E-mails duplicados identificados: {duplicados}"
    )
    print(p1)
    resultados.append(p1)

    # Pergunta 2: top 5 cargos
    top5 = df[df["cargo"] != "Desconhecido"]["cargo"].value_counts().head(5)
    p2_lines = ["2. Top 5 cargos mais frequentes:"]
    for cargo, count in top5.items():
        p2_lines.append(f"   - {cargo}: {count}")
    p2 = "\n".join(p2_lines)
    print(p2)
    resultados.append(p2)

    # Pergunta 3: empresas únicas
    empresas_unicas = df["empresa_harmonizada"].nunique()
    p3 = f"3. Empresas únicas (após harmonização): {empresas_unicas}"
    print(p3)
    resultados.append(p3)

    # Pergunta 4: empresa mais recorrente
    mais_recorrente = df["empresa_harmonizada"].value_counts().idxmax()
    mais_recorrente_count = df["empresa_harmonizada"].value_counts().max()
    p4 = f"4. Empresa mais recorrente: '{mais_recorrente}' com {mais_recorrente_count} leads"
    print(p4)
    resultados.append(p4)

    # Pergunta 5: leads por país (Brasil / México / Outros)
    por_pais = df["pais_padronizado"].value_counts()
    p5_lines = ["5. Leads por país (Brasil / México / Outros):"]
    for pais, count in por_pais.items():
        pct = count / len(df) * 100
        p5_lines.append(f"   - {pais}: {count} ({pct:.1f}%)")
    p5 = "\n".join(p5_lines)
    print(p5)
    resultados.append(p5)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("=== ANÁLISE EXPLORATÓRIA — PROJETO 3 PREPARA PORTUGAL ===\n\n")
        f.write("\n\n".join(resultados))
        f.write("\n")

    print(f"\nResultados guardados em: {OUT_PATH}")


if __name__ == "__main__":
    main()
