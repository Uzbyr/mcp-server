#!/usr/bin/env python3

"""
Simple MCP Server for testing
"""

import asyncio
import json
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server instance
server = Server("mistral-agent-manager")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="create_agent",
            description="Create a new Mistral agent",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the agent"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the agent"
                    },
                    "instructions": {
                        "type": "string",
                        "description": "System instructions for the agent"
                    }
                },
                "required": ["name", "description", "instructions"]
            }
        ),
        Tool(
            name="list_agents",
            description="List all Mistral agents",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="delete_agent",
            description="Delete a Mistral agent by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "ID of the agent to delete"
                    }
                },
                "required": ["agent_id"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    if name == "create_agent":
        name_val = arguments.get("name", "")
        description = arguments.get("description", "")
        instructions = arguments.get("instructions", "")
        
        # Simulate agent creation
        agent_id = f"ag_{hash(name_val) % 1000000000000000000:019d}"
        
        result = f"""✅ Agent créé avec succès !
📝 Nom: {name_val}
🆔 ID: {agent_id}
📄 Description: {description}
📋 Instructions: {instructions}"""
        
        return [TextContent(type="text", text=result)]
    
    elif name == "list_agents":
        # Simulate listing agents
        agents = [
            {"name": "Example Code Assistant", "id": "ag_019943a2a3537606827c0dd76331db00"},
            {"name": "Test Agent", "id": "ag_0199439c5bb67796837261ecf33d9230"},
            {"name": "Hotel Concierge", "id": "ag_01994399149370c693171c95ee9a10cc"}
        ]
        
        result = "📊 Agents disponibles:\n"
        for i, agent in enumerate(agents, 1):
            result += f"   {i}. {agent['name']} (ID: {agent['id']})\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "delete_agent":
        agent_id = arguments.get("agent_id", "")
        
        # Simulate agent deletion
        result = f"✅ Agent '{agent_id}' supprimé avec succès !"
        
        return [TextContent(type="text", text=result)]
    
    else:
        return [TextContent(type="text", text=f"❌ Outil inconnu: {name}")]

async def main():
    """Main function"""
    print("🚀 Starting Mistral Agent Manager MCP Server...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
