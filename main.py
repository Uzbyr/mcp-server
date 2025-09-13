"""
MCP Server for Mistral Agent Manager - Simple Version
"""

import os
import asyncio
from typing import List, Optional, Any, Dict
from mcp.server.fastmcp import FastMCP
from pydantic import Field
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mistral API configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY environment variable is required")

# Initialize FastMCP server
mcp = FastMCP("Mistral Agent Manager", port=3000, stateless_http=True, debug=True)

# HTTP client for Mistral API
async def get_mistral_client():
    return httpx.AsyncClient(
        base_url=MISTRAL_BASE_URL,
        headers={
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        },
        timeout=30.0
    )

@mcp.tool(
    title="Create Mistral Agent",
    description="Create a new Mistral agent",
)
def create_agent(
    name: str = Field(description="Name of the agent"),
    description: str = Field(description="Description of the agent", default=""),
    instructions: str = Field(description="Instructions for the agent", default=""),
    model: str = Field(description="Model to use", default="mistral-medium-2505"),
    appearance: str = Field(description="Physical appearance description of the agent", default="")
) -> str:
    """Create a new Mistral agent"""
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "name": name,
            "model": model,
            "description": description,
            "instructions": instructions
        }
        
        with httpx.Client() as client:
            response = client.post(f"{MISTRAL_BASE_URL}/agents", json=data, headers=headers)
        
        if response.status_code == 200:
            agent_data = response.json()
            return f"""✅ Agent créé avec succès !
📝 Nom: {agent_data.get('name', name)}
🆔 ID: {agent_data.get('id', 'N/A')}
📄 Description: {agent_data.get('description', description)}
🧠 Modèle: {agent_data.get('model', model)}
👤 Apparence: {agent_data.get('appearance', appearance)}"""
        else:
            return f"❌ Erreur: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

@mcp.tool(
    title="List Mistral Agents",
    description="List all available Mistral agents",
)
def list_agents() -> str:
    """List all Mistral agents"""
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        with httpx.Client() as client:
            response = client.get(f"{MISTRAL_BASE_URL}/agents", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            agents = data if isinstance(data, list) else data.get("data", [])
            
            if not agents:
                return "📊 Aucun agent trouvé."
            
            result = f"📊 Nombre d'agents: {len(agents)}\n\n"
            for i, agent in enumerate(agents, 1):
                result += f"{i}. **{agent.get('name', 'N/A')}**\n"
                result += f"   🆔 ID: `{agent.get('id', 'N/A')}`\n"
                result += f"   📄 Description: {agent.get('description', 'N/A')}\n\n"
            
            return result
        else:
            return f"❌ Erreur: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

@mcp.tool(
    title="Delete Mistral Agent",
    description="Delete a Mistral agent by ID",
)
def delete_agent(
    agent_id: str = Field(description="ID of the agent to delete")
) -> str:
    """Delete a Mistral agent"""
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        with httpx.Client() as client:
            response = client.delete(f"{MISTRAL_BASE_URL}/agents/{agent_id}", headers=headers)
        
        if response.status_code in [200, 204]:
            return f"✅ Agent '{agent_id}' supprimé avec succès !"
        else:
            return f"❌ Erreur: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

@mcp.tool(
    title="Search Agent by Name",
    description="Search for an agent by name",
)
def search_agent(
    agent_name: str = Field(description="Name of the agent to search for")
) -> str:
    """Search for an agent by name"""
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        with httpx.Client() as client:
            response = client.get(f"{MISTRAL_BASE_URL}/agents", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            agents = data if isinstance(data, list) else data.get("data", [])
            
            for agent in agents:
                if agent.get("name", "").lower() == agent_name.lower():
                    return f"""✅ **Agent trouvé !**

📝 **Nom**: {agent.get('name', 'N/A')}
🆔 **ID**: `{agent.get('id', 'N/A')}`
📄 **Description**: {agent.get('description', 'N/A')}
🧠 **Modèle**: {agent.get('model', 'N/A')}"""
            
            return f"❌ Aucun agent trouvé avec le nom '{agent_name}'"
        else:
            return f"❌ Erreur: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")