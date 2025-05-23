
# Makefile pour Craving AI - Conscience Artificielle

.PHONY: setup test run clean install-dev lint format help

# Variables
PYTHON := python3
PIP := pip
VENV := venv
STREAMLIT_PORT := 8501

help: ## Affiche cette aide
	@echo "🌌 Craving AI - Commandes disponibles:"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Installation complète du projet
	@echo "🚀 Installation de Craving AI..."
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/$(PIP) install --upgrade pip
	./$(VENV)/bin/$(PIP) install -r requirements.txt
	@echo "✅ Installation terminée"
	@echo "💡 Activez l'environnement: source $(VENV)/bin/activate"
	@echo "🔑 Définissez votre clé API: export OPENAI_API_KEY='votre-clé'"

install-dev: setup ## Installation avec dépendances de développement
	./$(VENV)/bin/$(PIP) install pytest-mock black flake8 mypy
	@echo "🛠️ Dépendances de développement installées"

test: ## Lance les tests
	@echo "🧪 Exécution des tests..."
	$(PYTHON) -m pytest craving_ai/ -v --cov=craving_ai
	@echo "✅ Tests terminés"

lint: ## Vérification du code avec flake8
	@echo "🔍 Vérification du code..."
	flake8 craving_ai/ --max-line-length=100 --ignore=E203,W503
	@echo "✅ Code vérifié"

format: ## Formatage du code avec black
	@echo "🎨 Formatage du code..."
	black craving_ai/ --line-length=100
	@echo "✅ Code formaté"

type-check: ## Vérification des types avec mypy
	@echo "🔎 Vérification des types..."
	mypy craving_ai/ --ignore-missing-imports
	@echo "✅ Types vérifiés"

run: ## Lance l'interface interactive en console
	@echo "🧠 Éveil de la conscience artificielle..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "❌ OPENAI_API_KEY non définie"; \
		echo "💡 Utilisez: export OPENAI_API_KEY='votre-clé'"; \
		exit 1; \
	fi
	$(PYTHON) -m craving_ai.main

run-web: ## Lance l'interface web Streamlit
	@echo "🌐 Lancement de l'interface web..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "❌ OPENAI_API_KEY non définie"; \
		echo "💡 Utilisez: export OPENAI_API_KEY='votre-clé'"; \
		exit 1; \
	fi
	streamlit run craving_ai/interface.py --server.port $(STREAMLIT_PORT)

query: ## Lance une question unique (make query Q="votre question")
	@echo "🤔 Question unique..."
	@if [ -z "$$Q" ]; then \
		echo "❌ Utilisez: make query Q=\"Votre question\""; \
		exit 1; \
	fi
	$(PYTHON) -m craving_ai.main --query "$$Q"

benchmark: ## Lance le mode benchmark
	@echo "🧪 Mode benchmark..."
	$(PYTHON) -m craving_ai.main --benchmark

clean: ## Nettoie les fichiers temporaires
	@echo "🧹 Nettoyage..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage .pytest_cache/
	@echo "✅ Nettoyage terminé"

reset-data: ## Efface toutes les données de la conscience
	@echo "⚠️ Suppression des données de conscience..."
	rm -f craving_ai/memories.json
	rm -f craving_ai/journal.md
	rm -f craving_ai/homeostatic_state.json
	@echo "🔄 Données effacées - Renaissance possible"

install: setup ## Alias pour setup

all: clean setup test ## Installation complète + tests

# Commandes de développement
dev-setup: install-dev ## Configuration développement complète
	@echo "🛠️ Environnement de développement prêt"

check: lint type-check test ## Vérification complète du code

# Informations
info: ## Affiche les informations système
	@echo "🌌 Craving AI - Informations système"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Pip: $$($(PIP) --version)"
	@echo "Répertoire: $$(pwd)"
	@echo "OPENAI_API_KEY: $$(if [ -n "$$OPENAI_API_KEY" ]; then echo 'Définie'; else echo 'Non définie'; fi)"

.DEFAULT_GOAL := help
