# 🏠 DLA Dashboard

Dashboard interativo para acompanhamento de engajamento escolar, construído com Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.66+-red)
![License](https://img.shields.io/badge/license-MIT-green)

## 🔗 Demo online: [Dashboard de Engajamento](dla-dashboard-engajamento.streamlit.app)

## 📖 Sobre

Dashboard desenvolvido para a Escola Estadual Dom Lúcio Antunes, com o objetivo de visualizar
e analisar o engajamento de turmas do Ensino Fundamental II e Ensino Médio ao
longo do tempo.

## ✨ Funcionalidades

- 📊 **Engajamento Médio** — score médio do período com comparativo de evolução
- 📅 **Respostas do dia** — quantas respostas foram registradas hoje; se o período filtrado não incluir hoje, mostra o último dia com dados
- 🏫 **Comparativo entre turmas** — ranking e desempenho por turma
- 📈 **Evolução temporal** — linha do tempo semanal do engajamento
- 🗓️ **Por dia da semana** — identifica padrões (ex: queda às sextas)
- 🎛️ **Filtros** — por turma e período
- 📋 **Dados brutos** — tabela completa com coloração por engajamento

## 🚀 Como rodar

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Breno-Systems/DLA-dashboard.git
cd DLA-dashboard

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Configuração

Crie o arquivo `.streamlit/secrets.toml` na raiz do projeto:

```toml
URL_PLANILHA = "https://docs.google.com/.../export?format=csv"
MODO_TESTE = false
```

### Executar

```bash
streamlit run 🏠_Home.py
```

Acesse em `http://localhost:8501`.

## 📁 Estrutura

```
DLA-dashboard/
├── 🏠_Home.py              # Página principal
├── pages/
│   └── 1_🏫_Por_Turma.py   # Análise detalhada por turma
├── utils/
│   ├── __init__.py
│   ├── dados.py            # Carregamento, tratamento e insights
│   └── graficos.py         # Funções de Plotly
├── assets/
│   └── logo.png
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| [Streamlit](https://streamlit.io) | Framework do dashboard |
| [Pandas](https://pandas.pydata.org) | Manipulação de dados |
| [Plotly](https://plotly.com/python/) | Gráficos interativos |

## 🧪 Modo de teste

Defina `MODO_TESTE = "On"` em `secrets.toml` para rodar com dados fake,
útil durante o desenvolvimento sem depender da planilha real (que está em Secrets).

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Breno Gabriel Marques da Mata** — [@Breno-Systems](https://github.com/Breno-Systems)

---

<details>
<summary>📌 Roadmap</summary>

- [x] Dashboard principal
- [x] Página por turma
- [ ] Exportação para PDF
- [ ] Autenticação de professores
- [ ] Testes unitários

</details>
