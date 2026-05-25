"""
Tarefa 1: Padronização de e-mail (lowercase, strip, validação, duplicados)
Tarefa 2: Padronização dos nomes das colunas (snake_case, sem acentos)
Tarefa 3: Padronize nomes próprios (Title Case, coluna nome_completo)
Tarefa 4: Padronizar nome das empresas (remoção de sufixos jurídicos)
Tarefa 5: Criar coluna país padronizado (Brasil / México / Outros)
"""

import re
import pandas as pd
from email_validator import validate_email, EmailNotValidError

RAW_PATH = "data/raw/leads_bruto.xlsx"
OUT_PATH = "data/processed/leads_harmonizados.xlsx"

# Mapeamento de nomes de colunas originais → snake_case sem acentos
COLUMN_RENAME = {
    "email": "email",
    "firstname": "primeiro_nome",
    "lastname": "sobrenome",
    "jobtitle": "cargo",
    "employeecompany": "empresa",
    "country": "pais",
    "googleaid": "googleaid",
}

LEGAL_SUFFIXES = re.compile(
    r"\b("
    r"INSTITUICAO DE PAGAMENTO|INSTITUIÇÃO DE PAGAMENTO|"
    r"SOCIEDADE DE CREDITO DIRETO|SOCIEDADE DE CRÉDITO DIRETO|"
    r"SOCIEDADE DE CR[…E]DITO[, FINANCIAMENTO E INVESTIMENTO]*|"
    r"SOLUCOES DE PAGAMENTO|SOLUÇÕES DE PAGAMENTO|"
    r"FINANCIAMENTO E INVESTIMENTO|"
    r"CR[…E]DITO[, ]*FINANCIAMENTO E INVESTIMENTO|"
    r"LTDA\.?|S\.A\.?|EIRELI|ME|EPP|SA"
    r")\b",
    flags=re.IGNORECASE,
)

DOMAIN_TO_COUNTRY = {
    ".com.br": "Brasil", ".net.br": "Brasil", ".org.br": "Brasil",
    ".gov.br": "Brasil", ".edu.br": "Brasil", ".io.br": "Brasil",
    ".mx": "México",
}

COUNTRY_NORMALIZE = {
    "Brazil": "Brasil",
    "brasil": "Brasil",
    "Mexico": "México",
    "méxico": "México",
}


def infer_country(pais_original, email: str) -> str:
    """Retorna Brasil, México ou Outros."""
    if isinstance(pais_original, str) and pais_original.strip():
        normalized = COUNTRY_NORMALIZE.get(pais_original.strip(), None)
        if normalized:
            return normalized
        # qualquer outro país com valor → Outros
        return "Outros"

    # sem país original → inferir pelo domínio do email
    if not isinstance(email, str) or "@" not in email:
        return "Outros"
    domain = email.split("@")[-1].lower()
    for suffix, country in DOMAIN_TO_COUNTRY.items():
        if domain.endswith(suffix):
            return country
    if domain.endswith(".br"):
        return "Brasil"
    if domain.endswith(".mx"):
        return "México"
    return "Outros"


def validate_email_address(email) -> bool:
    if not isinstance(email, str) or not email.strip():
        return False
    try:
        validate_email(email.strip(), check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def clean_company_name(name) -> str:
    if not isinstance(name, str):
        return "Desconhecido"
    cleaned = LEGAL_SUFFIXES.sub("", name)
    cleaned = re.sub(r"[,.\-]+\s*$", "", cleaned.strip())
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = cleaned.replace("…", "").strip()
    return cleaned.title() if cleaned else "Desconhecido"


def main():
    print("A carregar base bruta...")
    df = pd.read_excel(RAW_PATH)
    print(f"  {len(df)} registos, {len(df.columns)} colunas originais")

    # Tarefa 2: remover coluna 100% nula e renomear para snake_case
    df = df.drop(columns=["googleaid"])
    df = df.rename(columns={k: v for k, v in COLUMN_RENAME.items() if k in df.columns})
    print(f"  Colunas após renomeação: {list(df.columns)}")

    # Tarefa 1: padronizar e-mail
    df["email"] = df["email"].str.lower().str.strip()
    df["email_valido"] = df["email"].apply(validate_email_address)
    df["email_duplicado"] = df["email"].duplicated(keep=False) & df["email"].notna()
    n_invalidos = (~df["email_valido"]).sum()
    n_duplicados = df["email_duplicado"].sum()
    print(f"  E-mails válidos: {df['email_valido'].sum()} / {len(df)}")
    print(f"  E-mails inválidos/nulos: {n_invalidos}")
    print(f"  E-mails duplicados: {n_duplicados}")

    # Preencher nulos antes de processar
    df["cargo"] = df["cargo"].fillna("Desconhecido").str.strip()
    df["empresa"] = df["empresa"].fillna("Desconhecido").str.strip()
    df["sobrenome"] = df["sobrenome"].fillna("").str.strip()

    # Tarefa 3: padronizar nomes próprios
    df["primeiro_nome"] = df["primeiro_nome"].str.strip().str.title()
    df["sobrenome"] = df["sobrenome"].str.strip().str.title()
    df["nome_completo"] = (df["primeiro_nome"] + " " + df["sobrenome"]).str.strip()

    # Tarefa 4: harmonizar nomes de empresas
    df["empresa_harmonizada"] = df["empresa"].apply(clean_company_name)

    # Tarefa 5: coluna país padronizado (Brasil / México / Outros)
    df["pais_padronizado"] = df.apply(
        lambda row: infer_country(row["pais"], row["email"]), axis=1
    )
    print(f"\n  Distribuição de países:\n{df['pais_padronizado'].value_counts()}")

    df.to_excel(OUT_PATH, index=False)
    print(f"\nBase harmonizada guardada em: {OUT_PATH}")
    print(f"Colunas finais: {list(df.columns)}")


if __name__ == "__main__":
    main()
