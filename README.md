# Plano Estratégico do CCM — ARTESP

Apresentação do plano estratégico do Centro de Controle Multimodal da ARTESP: o que foi feito desde 2021 e o que se propõe. Publicada no GitHub Pages como página estática, com [reveal.js](https://revealjs.com/) vendorizado — sem framework de build, sem `npm`.

**Site:** `https://dorettoartesp.github.io/artest/`

## Como está organizado

| Pasta | O que é |
|---|---|
| `deck/` | **Fonte do conteúdo.** Um arquivo HTML por slide (`project/slides/<id>.html`) e o índice `project/deck.json` com a ordem. É uma cópia versionada do deck mantido como backup no claude.ai. |
| `site/` | **O que o Pages serve.** `index.html` é gerado a partir de `deck/`; `css/artesp.css` é a moldura com a identidade ARTESP; `vendor/reveal/` é o reveal.js 5.1.0; `img/` tem as logos. |
| `tools/build-site.py` | Conversor `deck/` → `site/index.html`. Troca os elementos próprios do formato de origem (`x-connector`, `x-shape`, `x-icon`) por SVG inline. |
| `output/vN/` | Exportações versionadas: PDF e PPTX exportados do backup no claude.ai. |
| `inputs/` | Material de apoio (TRs, planos, identidade visual). Ignorado pelo Git, salvo os arquivos de referência. |
| `site/docs/` | PDFs publicados para download: apresentação (PDF e PPTX), os três termos de referência e o Plano de Coleta de Dados. |

Os arquivos de memória de trabalho (`AGENTS.md`, `MEMORIA-PLANO-ESTRATEGICO.md`, `DESTAQUES-TRS-E-DIRETRIZES.md`, `OBSERVACOES-DECK.md`) existem só localmente e estão no `.gitignore`: o repositório é público.

## Fluxo de trabalho

```bash
make build   # deck/ -> site/index.html
make serve   # http://localhost:8080
make shots   # um PNG por slide em output/shots/ (requer google-chrome)
```

Para alterar a apresentação, edite o slide em `deck/project/slides/` e rode `make build`. Cada slide é um `<section>` de 1920×1080 com estilos inline; `deck/project/deck.json` define a ordem.

## Publicação

O GitHub Pages serve a branch **`gh-pages`**, que contém só o conteúdo de `site/`. Para publicar, depois de commitar em `main`:

```bash
make publish   # site/ -> branch gh-pages (git subtree) -> push
```

O pipeline em `.github/workflows/deploy.yml` faz o mesmo pelo GitHub Actions a cada `push` em `main`, mas depende de o Actions estar disponível na conta; a branch `gh-pages` funciona sem ele. O repositório é público: o site é público.

## Backup

O deck original está no claude.ai (tipo Slides) e permanece como backup; não é mais a fonte editada. As exportações feitas de lá ficam em `output/vN/`.
