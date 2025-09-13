# 🔌 MCP Server - Mistral Agent Manager

Ce dossier contient le serveur MCP (Model Context Protocol) pour la gestion des agents Mistral via Le Chat.

## 📁 Structure

```
mcp-server/
├── main.py                # Serveur MCP principal (FastMCP)
├── simple_server.py       # Serveur MCP simple (stdio)
├── test_mcp.py           # Tests du serveur MCP
├── pyproject.toml        # Configuration du projet
├── uv.lock              # Lock file des dépendances
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
   # Option 1: Serveur FastMCP (HTTP)
   uv run main.py
   
   # Option 2: Serveur simple (stdio)
   uv run python simple_server.py
   ```

## 🔧 Utilisation avec l'inspecteur MCP

1. **Lancer l'inspecteur :**
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **Se connecter au serveur :**
   - **Transport** : `stdio`
   - **Command** : `uv run python simple_server.py`
   - **Working Directory** : `/Users/yoandicosmo/Documents/LeChat MCP Hack/mcp-server`

3. **Ou utiliser HTTP :**
   - **Transport** : `Streamable HTTP`
   - **URL** : `http://127.0.0.1:3000/mcp`

## 🛠️ Outils disponibles

- ✅ **`create_agent`** - Créer un nouvel agent Mistral
- ✅ **`list_agents`** - Lister tous les agents
- ✅ **`delete_agent`** - Supprimer un agent par ID

## 🔗 Intégration avec Le Chat

Pour utiliser ce serveur MCP avec Le Chat :

1. **Configurer Le Chat** pour pointer vers ce serveur MCP
2. **Utiliser les outils** directement dans Le Chat pour gérer les agents Mistral
3. **Créer des agents** via des prompts naturels dans Le Chat

## 📖 Documentation

- **MCP Inspector** : http://localhost:6274 (quand l'inspecteur est lancé)
- **Documentation MCP** : https://modelcontextprotocol.io/