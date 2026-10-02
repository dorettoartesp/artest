.DEFAULT_GOAL := help

.PHONY: help install dev build export clean status

help: ## Exibe a lista de comandos disponíveis
	@echo ""
	@echo "Comandos disponíveis no Makefile:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

install: ## Instala as dependências do projeto via npm
	npm install

dev: ## Inicia o servidor local de desenvolvimento com hot-reload (http://localhost:3030)
	npm run dev

build: ## Compila a apresentação estática para publicação (gera pasta dist/)
	npm run build

export: ## Exporta a apresentação em formato PDF (requer Playwright instalado)
	npm run export

clean: ## Remove a pasta compilada (dist/)
	rm -rf dist

status: ## Exibe o status do Git e do repositório
	@git status
