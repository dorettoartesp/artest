# Design Spec: Estrutura Base de Apresentação Slidev com Deploy no GitHub Pages

- **Data:** 2026-10-02
- **Repositório Remoto:** `https://github.com/dorettoartesp/artest.git`
- **Ambiente:** Node.js v22+, npm 10+, Git 2.53+
- **Branch Principal:** `main`

---

## 1. Visão Geral e Objetivos

O objetivo deste projeto é disponibilizar uma infraestrutura limpa, moderna e versionada para criação de apresentações em slides baseadas em código (Slidev), com publicação contínua automatizada no GitHub Pages.

O repositório servirá como base para que o usuário armazene arquivos de apoio e repositórios clonados em uma pasta dedicada (`inputs/`) sem sujar o controle de versão, permitindo que outra inteligência artificial (LLM) processe essas fontes e alimente diretamente o arquivo de slides (`slides.md`).

---

## 2. Tecnologias e Dependências

- **Slidev (`@slidev/cli`)**: Gerador de slides interativos a partir de Markdown com suporte nativo a componentes Vue, diagramas Mermaid, formatação de código e transições.
- **Tema Slidev (`@slidev/theme-default`)**: Tema visual limpo, corporativo e responsivo.
- **GitHub Actions**: Pipeline CI/CD com `actions/deploy-pages@v4` e `actions/upload-pages-artifact@v3`.
- **GitHub Pages**: Hospedagem estática com base path configurada para `/artest/`.

---

## 3. Estrutura de Diretórios e Arquivos

```text
artesp-estrategia/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Workflow de build e publicação no GitHub Pages
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-10-02-slides-apresentacao-design.md
├── inputs/
│   ├── .gitkeep                # Garante que o diretório exista no clone
│   └── README.md               # Instruções sobre o uso da pasta como fonte para a LLM
├── public/
│   └── favicon.svg             # Ícone da apresentação
├── .gitignore                  # Regras de exclusão de artefatos e inputs
├── package.json                # Configuração npm, scripts e dependências
├── README.md                   # Instruções de instalação, execução e deploy
└── slides.md                   # Arquivo principal da apresentação com template ARTESP
```

---

## 4. Detalhamento dos Componentes

### 4.1. Configuração do Node e Dependências (`package.json`)
- **Scripts:**
  - `dev`: `slidev --open` (executa localmente na porta 3030 com reload automático)
  - `build`: `slidev build --base /artest/` (gera a saída estática em `dist/`)
  - `export`: `slidev export` (opcional, exporta slides para formato PDF)
- **Dependências de Desenvolvimento:**
  - `@slidev/cli`
  - `@slidev/theme-default`

### 4.2. Template de Slides (`slides.md`)
O arquivo inicial conterá:
- Metadados de frontmatter:
  ```yaml
  ---
  theme: default
  background: https://cover.sli.dev
  title: ARTESP - Estratégia
  info: |
    ## Apresentação Estratégica - ARTESP
    Documento e apresentação gerados via Slidev.
  class: text-center
  drawings:
    persist: false
  transition: slide-left
  mdc: true
  ---
  ```
- Slides de exemplo estruturados:
  1. **Capa:** Título institucional ("ARTESP - Planejamento Estratégico"), subtítulo e data.
  2. **Agenda:** Sumário em tópicos animados com `v-clicks`.
  3. **Pilares Estratégicos:** Layout em duas colunas (`layout: two-cols`) destacando objetivos e metas.
  4. **Fluxo e Governança:** Diagrama de fluxo com Mermaid integrado.
  5. **Próximos Passos:** Encerramento e contatos.
- Seção de ajuda comentada para instruir a outra LLM sobre as diretivas do Slidev.

### 4.3. Diretório de Fontes de Dados (`inputs/`)
- Diretório destinado a receber clones de outros repositórios Git, arquivos Markdown, documentos de texto e PDFs.
- **Regra no `.gitignore`:**
  ```gitignore
  inputs/*
  !inputs/.gitkeep
  !inputs/README.md
  ```
- Garante isolamento: repositórios clonados em `inputs/` não gerarão avisos de *nested git repository* nem serão acidentalmente comitados.

### 4.4. Pipeline de CI/CD (`.github/workflows/deploy.yml`)
- **Gatilhos:**
  - `push` na branch `main`
  - `workflow_dispatch` (acionamento manual pela interface do GitHub)
- **Permissões:** `pages: write`, `id-token: write`, `contents: read`.
- **Etapas do Job:**
  1. Checkout do código (`actions/checkout@v4`).
  2. Configuração do Node 22 com cache npm (`actions/setup-node@v4`).
  3. Instalação limpa (`npm ci` ou fallback para `npm install`).
  4. Build com base path `/artest/` (`npm run build`).
  5. Upload do artefato para o Pages (`actions/upload-pages-artifact@v3`).
  6. Deploy no GitHub Pages (`actions/deploy-pages@v4`).

### 4.5. Configuração do Git
- Inicialização local: `git init -b main`.
- Remoto configurado: `git remote add origin https://github.com/dorettoartesp/artest.git`.
- Primeiro commit contendo a estrutura base pronta.

---

## 5. Critérios de Sucesso e Verificação

1. **Estrutura criada:** Todos os arquivos de configuração, diretórios e templates estão no lugar.
2. **Build local executável:** `npm install` roda com sucesso e `npm run build` gera a pasta `dist/` sem erros de sintaxe ou dependências faltantes.
3. **Isolamento de `inputs/`:** Um arquivo temporário de teste dentro de `inputs/` é ignorado pelo `git status`.
4. **Git inicializado:** O repositório está na branch `main`, com o commit inicial registrado e o remote `origin` apontando para `https://github.com/dorettoartesp/artest.git`.
