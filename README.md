# Apresentação Estratégica ARTESP (Slidev)

Este repositório contém a infraestrutura e os slides da apresentação institucional da ARTESP, construída com [Slidev](https://sli.dev/) e publicada automaticamente no **GitHub Pages**.

🔗 **Apresentação Online:** `https://dorettoartesp.github.io/artest/`

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Node.js v20+ ou v22+
- npm instalado

### Instalação
```bash
make install   # ou npm install
```

### Iniciar Servidor de Apresentação (com hot-reload)
```bash
make dev       # ou npm run dev
```
Acesse `http://localhost:3030` no navegador.

### Gerar Build Estática
```bash
make build     # ou npm run build
```
Os arquivos prontos para publicação serão gerados no diretório `dist/` com o prefixo `/artest/`.

---

## 📂 Como Adicionar Conteúdo de Apoio (`inputs/`)

A pasta `inputs/` está configurada para receber materiais externos sem interferir no controle de versão Git:
1. Clone repositórios necessários dentro de `inputs/` (`git clone ... inputs/repo-nome`).
2. Copie relatórios, arquivos `.md`, notas ou documentos para `inputs/`.
3. Utilize uma LLM para analisar os arquivos contidos em `inputs/` e estruturar ou editar o arquivo `slides.md`.

---

## 🌐 Publicação Contínua (CI/CD)

O pipeline do GitHub Actions (`.github/workflows/deploy.yml`) compila os slides e atualiza o GitHub Pages automaticamente a cada `git push` na branch `main`.
