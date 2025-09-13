# 🌐 FastAPI Server - Mistral Agent Manager

Ce dossier contient le serveur FastAPI pour la gestion des agents Mistral via API REST.

## 📁 Structure

```
mcp-server/
├── main.py                # Serveur FastAPI principal
├── simple_server.py       # Serveur MCP simple (stdio) - ancien
├── test_mcp.py           # Tests du serveur MCP - ancien
├── pyproject.toml        # Configuration du projet
├── uv.lock              # Lock file des dépendances
├── .env                 # Variables d'environnement
├── .python-version      # Version Python
├── .gitignore          # Fichiers à ignorer
└── .venv/              # Environnement virtuel Python
```

## 🚀 Démarrage rapide

1. **Installer uv (si pas déjà fait) :**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. **Installer les dépendances :**
   ```bash
   cd mcp-server
   uv sync --locked
   ```

3. **Démarrer le serveur MCP :**
   ```bash
   uv run python main.py
   ```

## 🔧 Utilisation avec l'inspecteur MCP

1. **Lancer l'inspecteur :**
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **Se connecter au serveur :**
   - **Transport** : `stdio`
   - **Command** : `uv run python main.py`
   - **Working Directory** : `/Users/yoandicosmo/Documents/LeChat MCP Hack/mcp-server`

3. **Accéder à l'interface :**
   - **MCP Inspector** : http://localhost:6274 (quand l'inspecteur est lancé)

## 🛠️ Outils disponibles

- ✅ **`create_agent`** - Créer un nouvel agent Mistral
- ✅ **`list_agents`** - Lister tous les agents
- ✅ **`get_agent_details`** - Obtenir les détails d'un agent
- ✅ **`delete_agent`** - Supprimer un agent par ID
- ✅ **`search_agent`** - Rechercher un agent par nom

## 🔧 Configuration

1. **Variables d'environnement** : Configurez `MISTRAL_API_KEY` dans `.env`
2. **Transport** : Le serveur utilise stdio pour la communication MCP
3. **API Mistral** : Intégration complète avec l'API Mistral

## 🔗 Intégration avec Le Chat

Pour utiliser ce serveur MCP avec Le Chat :

1. **Configurer Le Chat** pour pointer vers ce serveur MCP
2. **Utiliser les outils** directement dans Le Chat pour gérer les agents Mistral
3. **Créer des agents** via des prompts naturels dans Le Chat

## 📖 Documentation

- **MCP Inspector** : http://localhost:6274 (quand l'inspecteur est lancé)
- **Documentation MCP** : https://modelcontextprotocol.io/