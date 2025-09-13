"""
MCP Server for Mistral Agent Manager
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
    description="Create a new Mistral agent with specified configuration",
)
def create_agent(
    name: str = Field(description="Name of the agent"),
    description: str = Field(description="Description of the agent", default=""),
    instructions: str = Field(description="Instruction prompt the model will follow", default=""),
    model: str = Field(description="Model to use", default="mistral-medium-2505"),
    temperature: float = Field(description="Temperature for completion", default=0.7),
    max_tokens: Optional[int] = Field(description="Maximum tokens to generate", default=None)
) -> str:
    """Create a new Mistral agent"""
    async def _create_agent():
        try:
            async with await get_mistral_client() as client:
                # Prepare the request body
                request_body = {
                    "name": name,
                    "model": model
                }
                
                if description:
                    request_body["description"] = description
                if instructions:
                    request_body["instructions"] = instructions
                
                # Add completion args
                completion_args = {}
                if temperature != 0.7:
                    completion_args["temperature"] = temperature
                if max_tokens:
                    completion_args["max_tokens"] = max_tokens
                
                if completion_args:
                    request_body["completion_args"] = completion_args
                
                response = await client.post("/agents", json=request_body)
                
                if response.status_code == 200:
                    agent_data = response.json()
                    return f"""✅ Agent créé avec succès !
📝 Nom: {agent_data.get('name', name)}
🆔 ID: {agent_data.get('id', 'N/A')}
📄 Description: {agent_data.get('description', description)}
🧠 Modèle: {agent_data.get('model', model)}
📋 Instructions: {agent_data.get('instructions', instructions)}
📅 Créé le: {agent_data.get('created_at', 'N/A')}"""
                else:
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = response.text
                    return f"❌ Erreur lors de la création de l'agent: {error_detail}"
        
        except Exception as e:
            return f"❌ Erreur de connexion à l'API Mistral: {str(e)}"
    
    # Run the async function
    return asyncio.run(_create_agent())

@mcp.tool(
    title="List Mistral Agents",
    description="List all available Mistral agents",
)
def list_agents() -> str:
    """List all Mistral agents"""
    async def _list_agents():
        try:
            async with await get_mistral_client() as client:
                response = await client.get("/agents")
                
                if response.status_code == 200:
                    data = response.json()
                    agents = data if isinstance(data, list) else data.get("data", [])
                    
                    if not agents:
                        return "📊 Aucun agent trouvé."
                    
                    result = f"📊 Nombre d'agents: {len(agents)}\n\n"
                    for i, agent in enumerate(agents, 1):
                        result += f"{i}. **{agent.get('name', 'N/A')}**\n"
                        result += f"   🆔 ID: `{agent.get('id', 'N/A')}`\n"
                        result += f"   📄 Description: {agent.get('description', 'N/A')}\n"
                        result += f"   🧠 Modèle: {agent.get('model', 'N/A')}\n"
                        result += f"   📅 Créé le: {agent.get('created_at', 'N/A')}\n\n"
                    
                    return result
                else:
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = response.text
                    return f"❌ Erreur lors de la récupération des agents: {error_detail}"
        
        except Exception as e:
            return f"❌ Erreur de connexion à l'API Mistral: {str(e)}"
    
    # Run the async function
    return asyncio.run(_list_agents())

@mcp.tool(
    title="Get Agent Details",
    description="Get detailed information about a specific agent",
)
def get_agent_details(
    agent_id: str = Field(description="ID of the agent to retrieve")
) -> str:
    """Get detailed information about a specific agent"""
    async def _get_agent_details():
        try:
            async with await get_mistral_client() as client:
                response = await client.get(f"/agents/{agent_id}")
                
                if response.status_code == 200:
                    agent_data = response.json()
                    return f"""📋 **Détails de l'agent**

📝 **Nom**: {agent_data.get('name', 'N/A')}
🆔 **ID**: `{agent_data.get('id', 'N/A')}`
📄 **Description**: {agent_data.get('description', 'N/A')}
🧠 **Modèle**: {agent_data.get('model', 'N/A')}
📋 **Instructions**: {agent_data.get('instructions', 'N/A')}
🔧 **Outils**: {len(agent_data.get('tools', []))} outil(s) configuré(s)
⚙️ **Arguments de complétion**: {agent_data.get('completion_args', 'Aucun')}
📅 **Créé le**: {agent_data.get('created_at', 'N/A')}
🔄 **Mis à jour le**: {agent_data.get('updated_at', 'N/A')}"""
                elif response.status_code == 404:
                    return f"❌ Agent avec l'ID '{agent_id}' non trouvé"
                else:
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = response.text
                    return f"❌ Erreur lors de la récupération de l'agent: {error_detail}"
        
        except Exception as e:
            return f"❌ Erreur de connexion à l'API Mistral: {str(e)}"
    
    # Run the async function
    return asyncio.run(_get_agent_details())

@mcp.tool(
    title="Delete Mistral Agent",
    description="Delete a Mistral agent by ID",
)
def delete_agent(
    agent_id: str = Field(description="ID of the agent to delete")
) -> str:
    """Delete a Mistral agent"""
    async def _delete_agent():
        try:
            async with await get_mistral_client() as client:
                response = await client.delete(f"/agents/{agent_id}")
                
                if response.status_code in [200, 204]:
                    return f"✅ Agent '{agent_id}' supprimé avec succès !"
                elif response.status_code == 404:
                    return f"❌ Agent avec l'ID '{agent_id}' non trouvé"
                else:
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = response.text
                    return f"❌ Erreur lors de la suppression de l'agent: {error_detail}"
        
        except Exception as e:
            return f"❌ Erreur de connexion à l'API Mistral: {str(e)}"
    
    # Run the async function
    return asyncio.run(_delete_agent())

@mcp.tool(
    title="Search Agent by Name",
    description="Search for an agent by name and get its ID",
)
def search_agent(
    agent_name: str = Field(description="Name of the agent to search for")
) -> str:
    """Search for an agent by name"""
    async def _search_agent():
        try:
            async with await get_mistral_client() as client:
                response = await client.get("/agents")
                
                if response.status_code == 200:
                    data = response.json()
                    agents = data if isinstance(data, list) else data.get("data", [])
                    
                    # Search for agent by name (case insensitive)
                    for agent in agents:
                        if agent.get("name", "").lower() == agent_name.lower():
                            return f"""✅ **Agent trouvé !**

📝 **Nom**: {agent.get('name', 'N/A')}
🆔 **ID**: `{agent.get('id', 'N/A')}`
📄 **Description**: {agent.get('description', 'N/A')}
🧠 **Modèle**: {agent.get('model', 'N/A')}
📅 **Créé le**: {agent.get('created_at', 'N/A')}

💡 **Vous pouvez maintenant utiliser l'ID `{agent.get('id', 'N/A')}` pour d'autres opérations.**"""
                    
                    return f"❌ Aucun agent trouvé avec le nom '{agent_name}'"
                else:
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = response.text
                    return f"❌ Erreur lors de la recherche de l'agent: {error_detail}"
        
        except Exception as e:
            return f"❌ Erreur de connexion à l'API Mistral: {str(e)}"
    
    # Run the async function
    return asyncio.run(_search_agent())

@mcp.resource(
    uri="mistral://agents",
    description="List all Mistral agents as a resource",
    name="Mistral Agents Resource",
)
def get_agents_resource() -> str:
    """Get all agents as a resource"""
    return asyncio.run(list_agents())

@mcp.prompt("")
def create_agent_prompt(
    name: str = Field(description="The name of the agent to create"),
    description: str = Field(description="Description of what the agent should do", default=""),
    instructions: str = Field(description="Specific instructions for the agent", default=""),
    model: str = Field(description="Mistral model to use", default="mistral-medium-2505")
) -> str:
    """Generate a prompt for creating a Mistral agent"""
    return f"""Create a Mistral agent with the following specifications:

**Agent Name**: {name}
**Description**: {description or "A helpful AI assistant"}
**Instructions**: {instructions or "You are a helpful AI assistant that follows instructions carefully."}
**Model**: {model}

Please use the create_agent tool to create this agent with the specified parameters."""

if __name__ == "__main__":
    mcp.run(transport="streamable-http")