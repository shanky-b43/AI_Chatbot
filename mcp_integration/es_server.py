import asyncio
import json
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.retriever import retrieve_context

# Create the MCP Server
server = Server("ai-chatbot-es-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools for interacting with Elasticsearch.
    """
    return [
        types.Tool(
            name="search_documents",
            description="Searches the Elasticsearch knowledge base to answer questions about company policies, IT guides, and general knowledge.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to retrieve relevant documents."
                    },
                    "sub_node": {
                        "type": "string",
                        "description": "Optional sub-node identifier to filter documents by specific department sub-nodes."
                    }
                },
                "required": ["query"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if name == "search_documents":
        if not arguments or "query" not in arguments:
            raise ValueError("Missing 'query' argument")
        
        query = arguments["query"]
        sub_node = arguments.get("sub_node")
        
        try:
            # We use the retrieve_context wrapper which gets top-k and formats them
            result = retrieve_context(query, sub_node=sub_node)
            return [types.TextContent(type="text", text=result)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error searching Elasticsearch: {str(e)}")]
            
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """
    Run the server using stdin/stdout streams.
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-chatbot-es-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
