# Projeto 3: Harmonização, Análise e Visualização da Base de Leads

> Projeto Final do curso **Análise de Dados e TI Aplicado à Gestão** da Prepara Portugal.  
> Limpeza, harmonização e análise exploratória de uma base de leads B2B para uso em CRM e BI.

---

## Identificação

| Campo | Valor |
|-------|-------|
| **Aluno** | Gustavo Waltrick |
| **Turma** | Turma F — Análise de Dados e TI Aplicado a Gestão — Lisboa |
| **Formadores** | Pedro Azeredo Coutinho Stob e Marcelo Ferreira |
| **Curso** | Análise de Dados e TI Aplicado à Gestão (DTI) |
| **Projeto** | Opção 3 — Harmonização e Análise de Base de Leads |
| **Entrega** | PDF + Repositório público no GitHub |

---

## Objetivo

Receber uma base bruta de leads B2B (6.016 registos), aplicar um processo completo de harmonização e limpeza, conduzir análise exploratória orientada a perguntas de negócio, e produzir visualizações que apoiem a tomada de decisão em CRM e BI.

---

## Estrutura de Pastas

```
projeto3-prepara-portugal/
├── data/
│   ├── raw/                    # Base original (não modificada)
│   └── processed/              # Base harmonizada
├── scripts/
│   ├── 01_harmonizacao.py      # Limpeza e padronização
│   ├── 02_analise.py           # Análise exploratória
│   └── 03_visualizacoes.py     # Geração de gráficos
├── outputs/
│   ├── graficos/               # Gráficos exportados
│   └── projeto_final.pdf       # Documento final
├── docs/
│   └── relatorio.md            # Relatório em Markdown
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Stack Técnica

- **Python 3.13** — linguagem principal
- **Pandas** — manipulação e análise de dados
- **Matplotlib / Seaborn** — visualizações estáticas
- **OpenPyXL** — leitura/escrita de ficheiros Excel
- **email-validator / dnspython** — validação de e-mails
- **Unidecode** — normalização de texto (acentos e caracteres especiais)
- **Looker Studio** — dashboard interativo

---

## Como Executar

```bash
# 1. Clonar o repositório
git clone https://github.com/waltrickme/projeto3-prepara-portugal.git
cd projeto3-prepara-portugal

# 2. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar pipeline
python scripts/01_harmonizacao.py
python scripts/02_analise.py
python scripts/03_visualizacoes.py
```

---

## Status do Projeto

- [x] Setup do ambiente
- [x] Inspeção da base original
- [x] Harmonização (5 tarefas obrigatórias)
- [x] Análise exploratória (5 perguntas obrigatórias)
- [x] Visualizações (4 gráficos obrigatórios)
- [ ] Dashboard no Looker Studio *(opcional — não incluído)*
- [x] Documento final em PDF

---

## Contato

**Gustavo Waltrick**  
Email: Waltrickme@gmail.com  
GitHub: [@waltrickme](https://github.com/waltrickme)

---

## Licença

Este projeto está sob licença MIT.
